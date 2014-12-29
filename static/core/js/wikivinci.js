function getPageHeight(){
	return $("#page-content").height();
}

function triggerAuthenticatePopup(){
	var modal = $("#authenticateModal");
	modal.find("p#alert").show();
	modal.modal('toggle');
}

$(document).ready(function(){

	// get register form
	$("#authenticateModal a#register").on("click", function(e){
		e.preventDefault();
		var popup_modal = $("#authenticateModal");
		var url = $(this).attr("href");
		$.ajax({
			url: url,
			type: "GET",
			success: function(response){
				popup_modal.find("form").hide();
				popup_modal.find(".modal-footer").hide();
				popup_modal.find(".modal-title").text("Sign up for Wikivinci!");
				popup_modal.find(".modal-body").append(response);
			}
		});
	});

	// submit ajax register form
	$("#authenticateModal").on("submit", "form#register", function(e){
		e.preventDefault();
		var modal_node = $("#authenticateModal");
		var form = $(this);
		var data = form.serializeArray()
		$.ajax({
			type: form.attr("method"),
			url: form.attr("action"),
			data: data,
			success: function(response){
				if (response != "success"){
					form.remove();
					modal_node.find(".modal-body").append(response);
					return;
				} else {
					location.reload();
				}
			}
		});		
	});

	// login via ajax
	$("#authenticateModal form#login").on("submit", function(e){
		e.preventDefault();
		var form = $(this);
		$.ajax({
			type: form.attr("method"),			
			url: form.attr("action"),
			data: {
				username: form.find("input[name='username']").val(),
				password: form.find("input[name='password']").val(),
			},
			success: function(response){
				if (response == "success") {
					location.reload();
				} else {
					form.find(".form-group input").addClass("error");
				}
			}
		});
	});

	// flag a post
	$("#flagPostModal #submit").on("click", function(){
		var modal_node = $("#flagPostModal");
		var edit = $.trim(modal_node.find("textarea").val())

		if (!(edit)) {
			modal_node.find("textarea").addClass("error");
			return;
		}

		var url = window.location.pathname + 'flag/';
		$.ajax({
			type: "POST",			
			url: url,
			data: {edit: edit},
			success: function(){
				modal_node.modal('toggle');
				modal_node.find('.modal-footer').remove();
				modal_node.find("p#explain").text("Your request has been submitted!")
				modal_node.find('textarea').prop('disabled', true);
			}
		});
	});

	// vote for comments and posts
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
					triggerAuthenticatePopup();
				}
			}
		});
	});
	
	// get the form
	$("#header a#add-post").on("click", function(){
		var popup_node = $("#post-add-popup");

		if (window.addPostFormHTML) {
			popup_node.find("form, #success").remove();
		}		

		$.ajax({
			type: 'GET',
			url: '/posts/add/',
			data: {},
			success: function(response, textStatus, xhr){
				popup_node.height(getPageHeight() + 100);
				popup_node.show();
				popup_node.animate({'right': '0px'});				
				popup_node.append(response);
				window.addPostFormHTML = true;
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403) {
					triggerAuthenticatePopup();
				}
			}
		});		
	});

	// hide the form
	$("#post-add-popup .x").on("click", function(){
		var popup_node = $("#post-add-popup");
		popup_node.animate({'right': '-3000px'}, function(){
			popup_node.hide();
		});
	});

	// submit the form
	$("#post-add-popup").on("submit", "form", function(e){
		e.preventDefault();

		var popup_node = $("#post-add-popup");
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
		var text = $.trim(form.find("textarea").val());

		if (!(text)) {
			form.find("textarea").addClass("error");
			return;
		}

		form.find("textarea").removeClass("error");
		$.ajax({
			type: "POST",			
			url: form.attr("action"),
			data: {
				post_id: post_id,
				text: text,
			},
			success: function(response, textStatus, xhr){
				if (response == "more points") {
					alert("You need more points before you can submit comments!");
					return;
				}
				location.reload();
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403) {
					triggerAuthenticatePopup();
				}
			}
		});
	});

	// delete comment
	$("#comments .comment a#delete").on("click", function(e){
		e.preventDefault();
		var comment_node = $(this).closest(".comment");
		var url = $(this).attr("href");
		var object_id = $(this).data("object-id");
		$.ajax({
			type: "POST",			
			url: url,
			data: {object_id: object_id},
			success: function(response){
				comment_node.fadeOut();
			}
		});
	});

});