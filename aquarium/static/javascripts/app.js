(function($){
  $(function(){

    $(document).foundationAlerts();
    // $(document).foundationAccordion();
    // $(document).tooltips();
    $('input, textarea').placeholder();



    $(document).foundationButtons();



    // $(document).foundationNavigation();



    // $(document).foundationCustomForms();




    $(document).foundationTabs({callback:$.foundation.customForms.appendCustomMarkup});

  });

})(jQuery);

// For index.html
$(function() {
    if ($('#index-table').length) {
        $("#index-table").append(jsonToTable(index_data));
    }
})

// For log.html
$(function () {
    if($("#log-table").length){
        $("#log-table").append(jsonToTable(log_data));
        plotJson(log_data, document.getElementById('plotholder'));
    }
});

// For script.html
$(function () {
    if($("#script-table").length){
        $("#script-table").append(jsonToTable(script_data));
    }
});

// For ajax.html
$(".spinner").hide();
$(function () {
    $(".results").hide();
    $(".ajax-control").each(function() {
        var $control = $(this);
        button_click($control);
        results_hide ($control);

    });

    function results_hide ($control) {
        var title = $control.find('.name');
        var results = $control.find('.results');
        $(title).click(function() {
            results.slideToggle();
        });
    }

    function button_click ($control) {
        $control.find(".run-button").click(function() {
            var runURL = $(this).attr('href');
            var $button = $(this);
            $button.hide();
            $control.find('.spinner').show();
            var $results = $control.find(".results");
            $results.slideUp();
            $results.load(runURL, {}, function() {
                $results.slideDown();
                $button.show();
                $control.find('.spinner').hide();
            });
        });
    }
});

function plotJson(json, holder){
    $.each(json, function(index, data) {
        var container = document.createElement("div");
        var title = document.createElement("h4");
        title.innerHTML = index;
        container.appendChild(title);
        var button = document.createElement("button")
        var plot = document.createElement("div");
        plot.style.width = "100%";
        plot.style.height = "300px";
        plot.id = "plot-" + index;
        container.appendChild(plot);
        holder.appendChild(container);

        var graph_data = []
        for (var t = 0; t < data.length; t += 1){
            graph_data.push([t, parseInt(data[t], 10)]);
        }

        function rand () {
             return Math.floor(Math.random()*255);
        }

        var rgb = 'rgb('+rand()+','+rand()+','+rand()+')'
        $.plot($("#" + plot.id), [{data:graph_data, color:rgb}]);

    });
}

function jsonToTable (json) {
    var table = document.createElement("table");
    var head = document.createElement("thead");
    head.appendChild(document.createElement("tr"));
    var body = document.createElement("tbody");

    /* loop over each object in the array to create rows*/
    var rows = Array();
    var headers = Array();
    $.each(json, function(index, item){
        headers.push(index)
        $.each(item, function(index, cell) {
            rows[index] = rows[index] || Array();
            rows[index].push(cell);
        });
    });

    $.each(headers, function(index, header) {
        var cell = document.createElement("th");
        cell.innerHTML = header
        head.firstChild.appendChild(cell)
    });

    $.each(rows, function(index, values) {
        var row = document.createElement("tr");
        body.appendChild(row);
        $.each(values, function(index, value) {
            var cell = document.createElement("td");
            cell.innerHTML = value;
            body.lastChild.appendChild(cell);
        });
    });

    table.appendChild(head);
    table.appendChild(body);
    return table;
}
