function getPageHeight(){
	return $("#page-content").height();
}

$(document).ready(function(){
	
	// get the form
	$("#header a#add-post").on("click", function(){
		var popup_node = $("#add-post-popup");
		popup_node.height(getPageHeight() + 100);
		popup_node.show();
		popup_node.animate({'right': '0px'});

		$.ajax({
			type: 'GET',
			url: '/posts/add-link/',
			data: {},
			success: function(response) {
				popup_node.append(response)
			}
		});		
	});

	$("#add-post-popup").on("submit", "form", function(e){
		e.preventDefault();

		var popup_node = $("#add-post-popup");
		var form = $(this);
		$.ajax({
			type: 'POST',
			url: '/posts/add-link/',
			data: form.serializeArray(),
			success: function(response){
				popup_node.find("form").remove();
				popup_node.append(response);
			}
		});
	});

});