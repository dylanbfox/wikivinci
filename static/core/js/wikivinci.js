function getPageHeight(){
	return $("#page-content").height();
}

function triggerAuthenticatePopup(){
	var modal = $("#authenticateModal");
	modal.find("p#alert").show();
	modal.modal('toggle');
}

function disableForm(form, fake){
	var inputs = form.find(":input");
	var submit = form.find("input[type='submit']");
	var orig_submit_text = submit.val();
	
	submit.val("processing...");
	if (fake == true) {
		form.css({"opacity": "0.4", "pointer-events": "none"});
	} else {
		inputs.prop("disabled", true);
	}

	return function(){
		if (fake == true) {
			form.css({"opacity": "1.0", "pointer-events": "initial"});
		} else {
			inputs.prop("disabled", false);
		}
		submit.val(orig_submit_text);
	}
}

$(document).ready(function(){

	// (function(){
	// 	var recently_added_nodes = $($("#home #activity #recent-posts > div").get().reverse());
	// 	var fade_recently_added_nodes = recently_added_nodes.slice(-5);
	// 	fade_recently_added_nodes.hide();
	// 	// scroll through recently added resources on home page
	// 	fade_recently_added_nodes.each(function(index){
	// 		$(this).delay(5000*index).fadeIn(800);
	// 	});
	// })();

	// feed filter options
	$("#feed-filter select#skill-level-filter").on("change", function(){
		var skill_level = $(this).val();
		var url = $(this).closest("#feed-filter").data("feed-url");

		$("#feed .posts").css('opacity', '0.3');
		$.ajax({
			type: 'GET',
			url: url,
			data: {skill_level: skill_level},
			success: function(response){
				$("#feed .posts").remove();
				$("#feed").append(response);
			}
		});
	});

	// show mobile menu
	$("#header #mobile-menu-toggle").on("click", function(){
		$("#header #links").show();
		$("#header #links").animate({'margin-right': '0px'});

		$("#page-content").one("click", function(){
			$("#header #links").animate({'margin-right': '-3000px'}, function(){
				$("#header #links").hide();
			});
		});
	});

	// filter posts by skill level
	$("select#skill-level-filter").on("change", function(){
		var posts = $(".posts .post");
		var skill_level = $(this).val();

		$(this).removeClass("filter-on");
		$("span#skill-level").text(skill_level);
		if (skill_level == "ALL"){
			posts.show();
			return;
		}

		posts.hide();
		$(".posts .post[data-skill-level="+skill_level+"]").show();
		$(this).addClass("filter-on");
	});

	// account settings page controls
	$("form#account-edit a#change-profile-pic").on("click", function(){
		$("form#account-edit input#new-profile-pic").slideToggle();
	});

	// show account dropdown
	$("#header a#auth").on("mouseenter", function(){
		$("#header #account-dropdown").show();
	});

	// show profile tooltip
	$(".profile-hover-toggle").on("mouseenter", function(){
		var target_id = $(this).data("target");
		var target_tooltip_node = $(target_id);
		var left_offset = $(this).position().left-305;
		target_tooltip_node.css('left', left_offset);
		target_tooltip_node.show();

		target_tooltip_node.on("mouseleave", function(){
			$(this).hide();
		});
	});

	$("#header .container #links > a").not("#auth").on("mouseenter", function(){
		if ($("this").attr("id") == "auth"){
			return;
		}
		$("#header #account-dropdown").hide();
	});

	$("#account-dropdown").on("mouseleave", function(){
		$("#header #account-dropdown").hide();
	});

	// authenticate popup - go back to login form
	$("#authenticateModal a#back-to-login").on("click", function(){
		var popup_modal = $("#authenticateModal");		
		popup_modal.find("form#register").hide();		
		popup_modal.find("form#login").show();
		popup_modal.find(".modal-footer a#back-to-login").hide();		
		popup_modal.find(".modal-footer a#register").show();
		popup_modal.find(".modal-title").text("Sign in to Wikivinci!");				
	});

	// get register form
	$("#authenticateModal a#register").on("click", function(e){
		e.preventDefault();
		var popup_modal = $("#authenticateModal");
		if (window.registerFormReceived) {
			popup_modal.find("form#login").hide();
			popup_modal.find(".modal-footer a#register").hide();
			popup_modal.find(".modal-footer a#back-to-login").show();
			popup_modal.find(".modal-title").text("Sign up for Wikivinci!");			
			popup_modal.find("form#register").show();
			return;							
		}

		var url = $(this).attr("href");
		$.ajax({
			url: url,
			type: "GET",
			success: function(response){
				popup_modal.find("form#login").hide();
				popup_modal.find(".modal-footer a#register").hide();
				popup_modal.find(".modal-footer a#back-to-login").show();
				popup_modal.find(".modal-title").text("Sign up for Wikivinci!");
				popup_modal.find(".modal-body").append(response);
				window.registerFormReceived = true;
			}
		});
	});

	// submit ajax register form
	$("#authenticateModal").on("submit", "form#register", function(e){
		e.preventDefault();
		var modal_node = $("#authenticateModal");
		var form = $(this);
		var data = form.serializeArray()

		disableForm(form);
		$.ajax({
			type: form.attr("method"),
			url: form.attr("action"),
			data: data,
			success: function(response){
				if (response != "success"){
					// append new form with errors
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

		enableForm = disableForm(form);
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
					enableForm();
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

		// prevent >1 vote from going through before ajax call completes
		count_node.closest(".votes-contain").attr("data-voted", "true");
		$.ajax({
			type: "POST",
			url: url,
			data: {vote_direction: vote_direction, object_id: object_id},
			success: function(response, textStatus, xhr){
				// update voting container
				count_node.closest(".votes-contain").addClass("voted");
				count_node.text(response);
			},
			error: function(xhr, textStatus, errorThrown){
				if (xhr.status == 403){
					// allow additional clicks, to trigger popup
					count_node.closest(".votes-contain").attr("data-voted", "false");					
					triggerAuthenticatePopup();
				}
			}
		});
	});
	
	// get the add post form
	$("a#add-post").on("click", function(){
		var popup_node = $("#post-add-popup");

		if (window.addPostFormHTML) {
			// remove everything and start from scratch
			popup_node.find("form, #success").remove();
		}		

		$.ajax({
			type: 'GET',
			url: '/posts/add/',
			data: {},
			success: function(response, textStatus, xhr){
				popup_node.height(getPageHeight() + 165);
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

	// hide the add post form
	$("#post-add-popup .x").on("click", function(){
		var popup_node = $("#post-add-popup");
		popup_node.animate({'right': '-3000px'}, function(){
			popup_node.hide();
		});
	});

	// submit the add post form
	$("#post-add-popup").on("submit", "form", function(e){
		e.preventDefault();

		var popup_node = $("#post-add-popup");
		var form = $(this);

		disableForm(form, fake=true);
		$.ajax({
			type: 'POST',
			url: '/posts/add/',
			data: form.serializeArray(),
			success: function(response){
				// append new form w errors or success msg
				popup_node.find("form").remove();
				popup_node.append(response);
			}
		});
	});

	// auto-fill tags in add post form
	$("#post-add-popup").on("keyup", "form input[name='tags']", function(){
		var all_chars = $(this).val();
		var comma_pos = all_chars.lastIndexOf(",");
		var suggested_topics_node = $("#post-add-popup #suggested-topics");

		suggested_topics_node.hide();
		suggested_topics_node.find("p").remove();			

		if (comma_pos != -1) {
			var chars = $.trim(all_chars.slice(comma_pos+1));			
		} else {
			var chars = all_chars;
		}

		if (chars.length < 2){
			return;
		}

		$.ajax({
			type: "POST",
			url: "/posts/topics/suggest/",
			data: {chars: chars},
			success: function(response){
				if (response.length < 1){
					return;
				}

				for (var i in response){
					suggested_topics_node.append($("<p>"+response[i]+"</p>"));
				}
				suggested_topics_node.show();				
			}
		});
	});

	// append suggested tag/topic on click
	$("#post-add-popup").on("click", "#suggested-topics > p", function(e){
		e.stopPropagation();
		var input_node = $("#post-add-popup form input[name='tags']");
		var current_val = input_node.val();
		var comma_pos = current_val.lastIndexOf(",");

		if (comma_pos == -1){
			var new_val = $(this).text();
		} else {
			var new_val = current_val.slice(0, comma_pos) + ", " + $(this).text();			
		}

		input_node.val(new_val);
		$("#post-add-popup #suggested-topics").hide();
	});

	// hide suggestions on blur
	$("#post-add-popup").on("click", "#suggested-topics #close", function(){
		$("#post-add-popup #suggested-topics").hide();
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
				if (response == "denied") {
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

	// toggle profile activity feeds
	$("#profile #activity #ops a").on("click", function(){
		var target_id = $(this).data("target");
		var feed_node = $(target_id);

		$("#profile #activity #ops a").removeClass("active")
		$("#profile #activity .feed").hide();
		$(this).addClass("active");
		feed_node.show();
	});

	// build out ajax for feed personalization

});