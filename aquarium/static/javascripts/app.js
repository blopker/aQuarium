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




    // $("#featured").orbit();


    // UNCOMMENT THE LINE YOU WANT BELOW IF YOU WANT IE8 SUPPORT AND ARE USING .block-grids
    // $('.block-grid.two-up>li:nth-child(2n+1)').css({clear: 'left'});
    // $('.block-grid.three-up>li:nth-child(3n+1)').css({clear: 'left'});
    // $('.block-grid.four-up>li:nth-child(4n+1)').css({clear: 'left'});
    // $('.block-grid.five-up>li:nth-child(5n+1)').css({clear: 'left'});
  });

})(jQuery);

function plotJson(json, holder){
    $.each(json, function(index, data) {
        var container = document.createElement("div");
        var title = document.createElement("h4");
        title.innerHTML = index;
        // container.appendChild(title);
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

        $.plot($("#" + plot.id), [graph_data]);

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
