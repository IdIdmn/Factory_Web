document.addEventListener("DOMContentLoaded", function () {
    
    var search_options = document.getElementById("search-options")
    if(search_options){
        function updateInputFields() {
            const text_input_fields = ["order_type"]
            const interval_input_fields = ["date_interval", "cost"]
            const date_input_fields = ["date"]
            if (date_input_fields.includes(search_options.value)){
                document.getElementById("text-input").style.display = "inline-block"                
                document.getElementById("interval-start-input").style.display = "none"
                document.getElementById("interval-end-input").style.display = "none"
                document.getElementById("text-input").value = ""
                document.getElementById("interval-start-input").value = ""
                document.getElementById("interval-end-input").value = ""
            } else if (interval_input_fields.includes(search_options.value)){
                document.getElementById("text-input").style.display = "none"   
                document.getElementById("interval-start-input").style.display = "inline-block"
                document.getElementById("interval-end-input").style.display = "inline-block"
                document.getElementById("text-input").value = ""
                document.getElementById("interval-start-input").value = ""
                document.getElementById("interval-end-input").value = ""
            } else if (text_input_fields.includes(search_options.value)) {
                document.getElementById("text-input").style.display = "inline-block"
                document.getElementById("interval-start-input").style.display = "none"
                document.getElementById("interval-end-input").style.display = "none"
                document.getElementById("text-input").value = ""
                document.getElementById("interval-start-input").value = ""
                document.getElementById("interval-end-input").value = ""
            }

            if (search_options.value == "cost"){
                document.getElementById("interval-start-input").setAttribute("placeholder", "начало диапазона")
                document.getElementById("interval-end-input").setAttribute("placeholder", "конец диапазона")
            } else if (search_options.value == "order_type"){
                document.getElementById("text-input").setAttribute("placeholder", "ремонт")
            } else if (search_options.value == "date_interval"){
                document.getElementById("interval-start-input").setAttribute("placeholder", "начальная дата (дд.мм.гггг)")
                document.getElementById("interval-end-input").setAttribute("placeholder", "конечная дата (дд.мм.гггг)")
            } else if (search_options.value == "date"){
                document.getElementById("text-input").setAttribute("placeholder", "дд.мм.гггг")
            } else if (search_options.value == "email"){
                document.getElementById("text-input").setAttribute("placeholder", "example@mail.ru")
            }
        }

        // updateInputFields();

        window.addEventListener("load", updateInputFields);
        search_options.addEventListener("change", updateInputFields);
    }

    let i = 1
    let row
    row = document.getElementById(`table-row-${i}`)
    while (row !== null) {
        let current_id = i
        let current_row = row
        current_row.addEventListener('mouseenter',  function() {
            let row_buttons_container = document.getElementById(`row-buttons-${current_id}`);
            if (row_buttons_container) {
                row_buttons_container.style.display = "block"; 
            }
        });
        current_row.addEventListener('mouseleave',  function() {
            let row_buttons_container = document.getElementById(`row-buttons-${current_id}`);
            if (row_buttons_container) {
                row_buttons_container.style.display = "none"; 
            }
        });
        i++;
        row = document.getElementById(`table-row-${i}`)
    }

    var headers = document.querySelectorAll("th");
    headers.forEach(function(header) {
        header.addEventListener("click", function() {
            var link = this.querySelector("a"); 
            if (link) {
                event.preventDefault(); 
                window.location.href = link.href;
            } 
        }); 
    });

});