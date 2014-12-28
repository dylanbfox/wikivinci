function getPageHeight(){
	return $("#page-content").height();
}

$(document).ready(function(){

	$(".votes-contain i.fa").on("click", function(){
		if ($(this).closest(".votes-contain").data("voted") == true) {
			return;
		}

		var vote_direction = $(this).data("vote-direction");
		var object_id = $(this).closest(".votes-contain").data("object-id");
		var count_node = $(this).closest(".votes-contain").find(".count");

		$.ajax({
			type: "POST",
			url: "/posts/vote/",
			data: {vote_direction: vote_direction, object_id: object_id},
			success: function(response, textStatus, xhr){
				if (xhr.status == 200) {
					count_node.text(response);
					count_node.closest(".votes-contain").addClass("voted");
					count_node.closest(".votes-contain").attr("data-voted", "true");
				} else {
					alert("login!")
				}
			}
		});
	});
	
	// get the form
	$("#header a#add-post").on("click", function(){
		var popup_node = $("#add-post-popup");
		popup_node.height(getPageHeight() + 100);
		popup_node.show();
		popup_node.animate({'right': '0px'});

		if (window.addPostFormHTML) {
			return;
		}		

		$.ajax({
			type: 'GET',
			url: '/posts/add/',
			data: {},
			success: function(response) {
				popup_node.append(response);
				window.addPostFormHTML = true;
			}
		});		
	});

	// hide the form
	$("#add-post-popup .x").on("click", function(){
		var popup_node = $("#add-post-popup");
		popup_node.animate({'right': '-3000px'}, function(){
			popup_node.hide();
		});
	});

	// submit the form
	$("#add-post-popup").on("submit", "form", function(e){
		e.preventDefault();

		var popup_node = $("#add-post-popup");
		var form = $(this);
		$.ajax({
			type: 'POST',
			url: '/posts/add/',
			data: form.serializeArray(),
			success: function(response){
				popup_node.find("form").remove();
				popup_node.append(response);
			}
		});
	});

});