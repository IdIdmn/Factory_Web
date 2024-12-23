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
            }
        }

        // updateInputFields();

        window.addEventListener("load", updateInputFields);
        search_options.addEventListener("change", updateInputFields);
    }

    const connect_button = document.getElementById("nav-connect-btn")
    if (connect_button) {
        connect_button.addEventListener("click", function () {
            document.getElementById('connect-with-us-section').scrollIntoView();
        });
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