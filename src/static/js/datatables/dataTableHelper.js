var integrationHelper = {
    loadTableJobs: [],
    loadTable: function($container, min, max){

        var url = $container.attr('data-load-url');

        data = {
            start_date: min.getTime(),
            end_date: max.getTime(),
            to_init: true,
        }

        // abort previous jobs
        integrationHelper.loadTableJobs.forEach(function(job, i){
            if(job && job.readyState != 4){
                root.console.log('Abort one previous integration ajax job');
                job.abort();
            };
        });

        var job = loadURL(url, $container, data, "POST");

        integrationHelper.loadTableJobs.push(job);

        // assign ajax to container parent data for load more
        $container[0].ajaxData = {
            min: min,
            max: max,
            url: url,
        }
    },
    loadRow: function(node, $container, url, data){

        var $spinner = $('<i class="fa fa-refresh fa-spin" style="margin-right: 5px;">');
        $btn = $(node);

        if($btn.data('load') || $btn.data('load-sending')){
            return;
        }

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'html',
            async: true,
            data: data,
            beforeSend: function(xhr, settings){
                $spinner.prependTo($btn);
                $btn.data('load-sending', true);
                // CSRF token
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                }
            },
            compvare: function(){
                $btn.find('.fa-spinner').remove();
                $btn.data('load-sending', false);
            },
            error: function(){
                $btn.find('.fa-spinner').remove();
                $btn.data('load-sending', false);
            },
        }).done(function(data){
            var $trs = $(data);

            // INSERT ROWS
            var table = $container.DataTable();
            $trs.each(function(){
                $this = $(this);
                if($this.is('tr')) table.rows.add($this).draw();
            })

            $btn.text(gettext('All Result Successfully Loaded'));
            $btn.addClass('disabled');

            $tds = $trs.find('td[data-sparkline]');
            if($tds.length > 0 && doChunk){
                doChunk($tds);
            }

            dataTableHelper.compareIntegrationRow($container);

            // SET ATTRIBUTE
            $btn.data('load', true);

        }).fail(function(){
            root.console.log('Load Historical Data Failed');

            $btn.text(gettext('Load Failed') + ', ' + gettext('Retry'));
            $btn.find('.fa-spinner').remove();
            $btn.data('load-sending', false);
        })

    }
}

var dataTableHelper = {
    init: function(){
        if(thisDevice == 'desktop'){
            $.fn.DataTable.ext.pager.numbers_length = 7;
        }
        else{
            $.fn.DataTable.ext.pager.numbers_length = 4;
        }
    },
    responsiveHelpers: [],
    language: {
        sEmptyTable:     gettext("No data available in table"),
        sInfo:           gettext("Showing _START_ to _END_ of _TOTAL_ entries"),
        sInfoEmpty:      gettext("Showing 0 to 0 of 0 entries"),
        sInfoFiltered:   gettext("(filtered from _MAX_ total entries)"),
        sInfoPostFix:    "",
        sInfoThousands:  ",",
        sLengthMenu:     gettext("Show _MENU_ entries"),
        sLoadingRecords: gettext("Loading") + '...',
        sProcessing:     gettext("Processing") + '...',
        sSearch:         gettext("Search"),
        sZeroRecords:    gettext("No matching results found"),
        oPaginate: {
            sFirst:    gettext("First"),
            sLast:     gettext("Last"),
            sNext:     gettext("Next"),
            sPrevious: gettext("Previous"),
        },
        oAria: {
            sSortAscending:  gettext(": activate to sort column ascending"),
            sSortDescending: gettext(": activate to sort column descending"),
        },
        buttons: {
            copyTitle: gettext('Copy To Clipboard'),
            copySuccess: {
                _: gettext('Copy %d rows'),
                1: gettext('Copy 1 row'),
            },
        },
    },
    buttons: {
        copy: function(options){
            return $.extend(true, {extend: 'copy', text: gettext('Copy')}, options);
        },
        csv: function(options){
            return $.extend(true, {extend: 'csv', charset: 'UTF-16LE', bom: true, text: gettext('Download') + 'CSV'}, options);
        },
        excel: function(options){
            return $.extend(true, {extend: 'excel', text: gettext('Download') + 'Excel'}, options);
        },
        pdf: function(options){
            return $.extend(true, {extend: 'pdf', text: gettext('Download') + 'Pdf'}, options);
        },
        print: function(options){
            return $.extend(true, {extend: 'print', text: gettext('Print')}, options);
        },
        UI: '\
            <div class="row">\
                <div class="col-sm-12 col-md-12" style="padding-bottom:0.3rem;"></div>\
            </div>\
        ',
        create: function(table){
            var div = $(this.UI);
            var container = $(table.buttons().container());
            div.find('.col-md-12:eq(0)').html(container);
            div.appendTo($(table.table().container()));
        },
    },
    breakpointDefinition : {
        tabvar : 1024,
        phone : 480
    },
    createRaw: function(container){
        var responsiveHelper = null;
        this.responsiveHelpers.push(responsiveHelper);

        var $container = $('#'+ container);

        /* Trans Table To DataTable */
        var $table = $container.DataTable({
			dom: "<'dt-toolbar padding-10 padding-left-0'<'col-xs-12 col-sm-12 hidden-xs'B><'col-xs-12 col-sm-12 hidden-sm hidden-md hidden-lg'f>>"+
				 "t"+
				 "<'dt-toolbar-footer'<'col-sm-6 col-xs-12 hidden-xs'i><'col-xs-12 col-sm-6'p>>",
            buttons: [
                dataTableHelper.buttons.csv(),
                dataTableHelper.buttons.excel(),
                dataTableHelper.buttons.print(),
                dataTableHelper.buttons.copy(),
            ],
            number: 3,
			autoWidth : true,
			preDrawCallback : function() {
				// Initialize the responsive datatables helper once.
				if (!responsiveHelper) {
					responsiveHelper = new ResponsiveDatatablesHelper($container, dataTableHelper.breakpointDefinition);
				}
			},
			rowCallback : function(nRow) {
				responsiveHelper.createExpandIcon(nRow);
			},
			drawCallback : function(oSettings) {
				responsiveHelper.respond();
			},
            order: [
                [0, 'desc']
            ],
            language: dataTableHelper.language,
        });

	    // Apply the filter
	    $("#" + container + " thead th input[type=text]").on( 'keyup change', function () {

	        $table
	            .column( $(this).parent().index()+':visible' )
	            .search( this.value )
	            .draw();

	    } );

        return $table;

    },
    createIntegration: function(container){

        function getAjaxDataFromContainer($container){
            // Access ajax data from parent div
            $parent = $container.closest('div[data-load]');
            var ajaxData = $parent[0].ajaxData;
            return ajaxData;
        }

        $container =$('#' + container);

        var responsiveHelper = null;
        this.responsiveHelpers.push(responsiveHelper);

        var columnLength = $container.find('tbody > tr:first td').length;
        switch(columnLength){
            case 3:
                columns = [0, 1];
                break;
            case 5:
                columns = [0, 1, 3];
                break;
            case 7:
                columns = [0, 1, 3, 5];
                break;
            default:
                columns = null;
                break;
        }

        // exporting column options
        var btnOptions = {
            exportOptions: {
                columns: columns,
            }
        }
        buttons = [
            dataTableHelper.buttons.csv(btnOptions),
        ]

        if(thisDevice == 'desktop'){
            buttons.push(dataTableHelper.buttons.excel(btnOptions)),
            buttons.push(dataTableHelper.buttons.print(btnOptions)),
            buttons.push(dataTableHelper.buttons.copy(btnOptions))
        }

        var ajaxData = getAjaxDataFromContainer($container);

        // Add btnLoad if start date and end date in same year
        sameYear = ajaxData.min.getYear() == ajaxData.max.getYear();
        btnLoadRow = sameYear ? {
            text: gettext('Load Historical Data'),
            action: function(e, dt, node){
                var typeId = $container.attr('data-type-id');
                var ajaxData = getAjaxDataFromContainer($container);
                var data = {
                    start_date: ajaxData.min.getTime(),
                    end_date: ajaxData.max.getTime(),
                    to_init: false,
                    type_id: typeId,
                }
                integrationHelper.loadRow(node, $container, ajaxData.url, data);
            },
        } : null
        if(sameYear) buttons.push(btnLoadRow);

        // adjust column width
        var columnLength = $container.find("tr:first th").length;
        var columnWidth = 100 / columnLength + '%';

        var columns = [];
        for(var i = 0; i < columnLength; i++){
            columns.push({ width: columnWidth });
        }

        var $table = $container.DataTable({
			dom: "<'dt-toolbar padding-10 padding-left-0'<'col-xs-12 col-sm-12'B>>"+
				 "t"+
				 "<'dt-toolbar-footer'>",
            buttons: buttons,
            paging: false,
			autoWidth : false,
			preDrawCallback : function() {
				// Initialize the responsive datatables helper once.
				if (!responsiveHelper) {
					responsiveHelper = new ResponsiveDatatablesHelper($container, dataTableHelper.breakpointDefinition);
				}
			},
			rowCallback : function(nRow) {
				responsiveHelper.createExpandIcon(nRow);
			},
			drawCallback : function(oSettings) {
				responsiveHelper.respond();
			},
			columns: columns,
            order: [
                [0, 'asc']
            ],
            language: dataTableHelper.language,
        });

        // sparkle line chunk
        $td = $container.find('td[data-sparkline]');
        if(doChunk && $td){
            doChunk($td);
        }

        dataTableHelper.compareIntegrationRow($container);

        return $table;
    },
    compareIntegrationRow: function(){
        $container.find('td[data-base="false"]').each(function(){
            $this = $(this);

            if($this.attr('data-compared')){
                return;
            }

            var columnNo = $this.index();
            $base = $this.closest("table").find("tr td:nth-child(" + (columnNo+1) + ")").filter('[data-base="true"]');
            if($base.length == 1){
                var thisValue = parseFloat($this.data('value'));
                var baseValue = parseFloat($base.data('value'));
                var diff = ((baseValue - thisValue) / thisValue) * 100;
                diff = Math.round(diff * 10) / 10;
                if(diff > 0){
                    var $ui = $('<span class="label bg-color-redLight pull-right hidden-xs hidden-sm"><i class="fa fa-caret-up"></i> '+ diff +'%</span>');
                }else{
                    var $ui = $('<span class="label bg-color-greenLight pull-right hidden-xs hidden-sm"><i class="fa fa-caret-down"></i> '+ diff * -1 +'%</span>');
                }
                $ui.appendTo($this);
            }

            $this.attr('data-compared', true);
        })
    },
    createEvent: function(container){
        var responsiveHelper = null;
        this.responsiveHelpers.push(responsiveHelper);

        var $container = $('#'+ container);
        var $form = $("#eventModal").find('form');

        var editable = $container.attr('data-editable') === 'editable';
        var btnOptions = {
            exportOptions: {
                columns: [2, 3, 4, 5, 6]
            }
        }
        var buttons = [
            dataTableHelper.buttons.csv(btnOptions),
            dataTableHelper.buttons.excel(btnOptions),
            dataTableHelper.buttons.print(btnOptions),
            dataTableHelper.buttons.copy(btnOptions),
        ];
        if(editable){
            // addEvent
            buttons.push({
                text: '<span><i class="fa fa-plus" aria-hidden="true"></i> ' + gettext('New Event') + '</span>',
                action: function(e, dt, node) {
                    $("#eventModal").find('form').attr('data-action', 'new');
                    $("#eventModal").find('.modal-title').text(gettext('New Event'));
                    $("#eventModal").find('form').formcontrol().reset();
                    $("#eventModal").find('form').formcontrol().data({
                        content_type: $form.attr('data-content-type'),
                        object_id: $form.attr('data-object-id'),
                    });
                    $("#eventModal").modal();
                },
            })
        }

        var table = $container.DataTable({
			dom: "<'dt-toolbar padding-10 padding-left-0'<'col-sm-6 hidden-xs'B><'col-xs-12 col-sm-6 hidden-sm'f>r>"+
				 "t"+
				 "<'dt-toolbar-footer'<'col-sm-6 col-xs-12 hidden-xs'i><'col-xs-12 col-sm-6'p>>",
            buttons: buttons,
			autoWidth : true,
            processing: true,
            serverSide: true,
            ajax: {
                url: $form.attr('data-url'),
                type: "GET",
                data: {
                    content_type: $form.attr('data-content-type'),
                    object_id: $form.attr('data-object-id'),
                    datatable: true,
                },
            },
            columns: [
                {
                    data: null,
                    defaultContent: '<button type="button" class="btn btn-xs btn-success btn-edit"><i class="fa fa-edit" aria-hidden="true"></i></button>',
                },
                {
                    data: null,
                    defaultContent: '<button type="button" class="btn btn-xs btn-danger btn-delete"><i class="fa fa-remove" aria-hidden="true"></i></button>',
                },
                {data: "date"},
                {data: "full_name"},
                {
                    data: "types",
                    render: "[, ].label",
                },
                {data: "name"},
                {
                    data: "context",
                    render: function(data, type, row){
                        return data.split("\n").join("<br/>");
                    },
                },
            ],
			preDrawCallback : function() {
				// Initialize the responsive datatables helper once.
				if (!responsiveHelper) {
					responsiveHelper = new ResponsiveDatatablesHelper($container, dataTableHelper.breakpointDefinition);
				}
			},
			rowCallback : function(nRow) {
				responsiveHelper.createExpandIcon(nRow);
			},
			drawCallback : function(oSettings) {
				responsiveHelper.respond();
			},
            language: dataTableHelper.language,
            order: [
                [2, 'desc']
            ],
            columnDefs: [
                {
                    targets: [0, 1, 3, 6], // edit, delete, user, context
                    createdCell:  function (td, cellData, rowData, row, col) {
                        $(td).attr('data-hide', 'phone');
                    },
                },
                {
                    targets: [0, 1], // edit, delete
                    visible: editable,
                },
                {
                    targets: [0, 1, 5, 6], // edit, delete, name, context
                    orderable: false,
                },
            ],
        });

        $container.find('tbody').on('click', 'button', function(){
            var $btn = $(this);
            var data = table.row($(this).parents('tr')).data();

            // DataTable first initial row data.types is array, then coerce to string
            data.types = Array.isArray(data.types) ? data.types.reduce(function(p, e){
                return p === '' ? e.label : p + ',' + e.label;
            }, '') : data.types;

            $form.formcontrol().data(data);

            if ($btn.hasClass('btn-edit')) {
                // EDIT button
                $form.attr('data-action', 'edit');
                $("#eventModal").find('.modal-title').text(gettext('Edit Event'));
                $("#eventModal").modal();
            } else {
                // DELETE button
                $form.attr('data-action', 'delete');
                $("#eventModal").find('.modal-title').text(gettext('Delete Event'));
                BootstrapDialog.confirm({
                    title: gettext('Delete Event'),
                    message: gettext('Are you sure you want to delete this event?'),
                    type: BootstrapDialog.TYPE_DANGER,
                    btnOKLabel: gettext('Delete'),
                    btnCancelLabel: gettext('Cancel'),
                    callback: function(result){
                        if(result) sendRequest();
                    },
                });
            }
        })

        $("#eventModal form").on('submit', function (e) {
            e.preventDefault();
            sendRequest();
        });

        var sendRequest = function() {

            var id = $form.formcontrol().data().id;
            var action = $form.attr('data-action');
            var method = null;
            var data = null;
            var url = $form.attr('data-url');

            switch(action){
                case "new":
                    method = 'POST';
                    data = $form.serialize();
                    break;
                case "edit":
                    url = url + id + '/';
                    method = 'PUT';
                    data = $form.serialize();
                    break;
                case "delete":
                    url = url + id + '/';
                    method = 'DELETE';
                    break;
            }

            $.ajax({
                url: url,
                method: method,
                data: data,
                beforeSend: function(xhr, settings) {
                    // CSRF token
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                    }
                },
            }).done(function (data, textStatus, jqXHR) {
                // DataTable data reload
                table.ajax.reload();
                // Highchart data reload
                if(window.chart5Helper) chart5Helper.loadEvents();

                if(($("#eventModal").data('bs.modal') || {}).isShown){
                    $("#eventModal").modal('toggle');
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                if(jqXHR.responseJSON){
                    $form.formcontrol().validate(jqXHR.responseJSON);
                }else{
                    console.log(jqXHR);
                }
            });

        }
        return table;
    },
}

dataTableHelper.init();