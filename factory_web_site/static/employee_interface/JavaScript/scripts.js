document.addEventListener("DOMContentLoaded", function () {
    
    var search_options = document.getElementById("search-options")
    if(search_options){
        function updateInputFields() {
            const text_input_fields = ["order_type", "date", "email", "phone_number", "full_name", "company_name", "vendor", "metal_type",
                 "metal_grade", "specialty", "serial_number", "machine_name", "material_id", "order_id", "employee_id", "machine_id", "start_date", "end_date"]
            const interval_input_fields = ["date_interval", "cost", "quantity"]
            const non_input_field = ["unprocessed_applications", "processed_applications"]
            if (interval_input_fields.includes(search_options.value)){
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
            } else if (non_input_field.includes(search_options.value)) {
                document.getElementById("text-input").style.display = "none"
                document.getElementById("interval-start-input").style.display = "none"
                document.getElementById("interval-end-input").style.display = "none"
                document.getElementById("text-input").value = ""
                document.getElementById("interval-start-input").value = ""
                document.getElementById("interval-end-input").value = ""
            }

            if (search_options.value == "cost" || search_options.value == "quantity"){
                document.getElementById("interval-start-input").setAttribute("placeholder", "начало диапазона")
                document.getElementById("interval-end-input").setAttribute("placeholder", "конец диапазона")
            } else if (search_options.value == "order_type"){
                document.getElementById("text-input").setAttribute("placeholder", "ремонт")
            } else if (search_options.value == "date_interval"){
                document.getElementById("interval-start-input").setAttribute("placeholder", "начальная дата (дд.мм.гггг)")
                document.getElementById("interval-end-input").setAttribute("placeholder", "конечная дата (дд.мм.гггг)")
            } else if (search_options.value == "date" || search_options.value == "start_date" || search_options.value == "end_date"){
                document.getElementById("text-input").setAttribute("placeholder", "дд.мм.гггг")
            } else if (search_options.value == "email"){
                document.getElementById("text-input").setAttribute("placeholder", "example@mail.ru")
            } else if (search_options.value == "phone_number"){
                document.getElementById("text-input").setAttribute("placeholder", "+7-916-839-47-68")
            } else if (search_options.value == "full_name"){
                document.getElementById("text-input").setAttribute("placeholder", "Иванов Иван Иванович")
            } else if (search_options.value == "company_name" || search_options.value == "vendor"){
                document.getElementById("text-input").setAttribute("placeholder", "")
            } else if (search_options.value == "metal_type"){
                document.getElementById("text-input").setAttribute("placeholder", "Сталь")
            } else if (search_options.value == "metal_grade"){
                document.getElementById("text-input").setAttribute("placeholder", "Ст2сп")
            } else if (search_options.value == "specialty"){
                document.getElementById("text-input").setAttribute("placeholder", "Токарь")
            } else if (search_options.value == "serial_number"){
                document.getElementById("text-input").setAttribute("placeholder", "XYZ1234567890")
            } else if (search_options.value == "machine_name"){
                document.getElementById("text-input").setAttribute("placeholder", "Токарный станок")
            } else if (search_options.value == "order_id"){
                document.getElementById("text-input").setAttribute("placeholder", "14")
            } else if (search_options.value == "material_id"){
                document.getElementById("text-input").setAttribute("placeholder", "41")
            } else if (search_options.value == "employee_id"){
                document.getElementById("text-input").setAttribute("placeholder", "62")
            } else if (search_options.value == "machine_id"){
                document.getElementById("text-input").setAttribute("placeholder", "38")
            } 
        }
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


    var side_menu_button = document.getElementById("nav-bar-menu-image")
    side_menu_button.addEventListener("click", function() {
        var nav_menu = document.getElementById("hidden-nav-menu")
        console.log("SMTH happened")
        if (nav_menu.style.width == "0px" || !nav_menu.style.width) {
            nav_menu.style.width = "300px"
        } else{
            nav_menu.style.width = "0px"
        }
    }); 
});