function getPageHeight(){
	return $("#page-content").height();
}

$(document).ready(function(){

	$(".votes-contain i.fa").on("click", function(){
		if ($(this).closest(".votes-contain").data("voted") == true){
			return;
		}

		var vote_direction = $(this).data("vote-direction");
		var object_id = $(this).closest(".votes-contain").data("object-id");
		var count_node = $(this).closest(".votes-contain").find(".count");
		var url = $(this).closest(".votes-contain").data("url");

		$.ajax({
			type: "POST",
			url: url,
			data: {vote_direction: vote_direction, object_id: object_id},
			success: function(response, textStatus, xhr){
				console.log(response);
				count_node.text(response);
				count_node.closest(".votes-contain").addClass("voted");
				count_node.closest(".votes-contain").attr("data-voted", "true");
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403){
					alert("login required!");
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
			success: function(response, textStatus, xhr){
				popup_node.append(response);
				window.addPostFormHTML = true;
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403) {
					alert("You need to login!");
				}
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

	// submit comment
	$("form#add-comment").on("submit", function(e){
		e.preventDefault();
		var form = $(this);
		var post_id = form.data("post-id");
		var text = form.find("textarea").val();

		$.ajax({
			url: form.attr("action"),
			type: "POST",
			data: {
				post_id: post_id,
				text: text,
			},
			success: function(response, textStatus, xhr){
				location.reload();
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403) {
					alert("You need to login first!");
				}
			}
		});
	});

});