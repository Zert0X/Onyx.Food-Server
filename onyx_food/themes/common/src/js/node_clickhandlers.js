function restaurant_node_click(clicked_id){
    const el = document.createElement("input");
    el.value = clicked_id.substring(11);
    el.name = "chosen_restaurant"
    el.id = "chosen_restaurant";
    el.hidden = true;

    const form = document.getElementById("restaurant_choose");
    form.appendChild(el);
    form.submit();
}