/* all javascript for site can go here */

/* for side accordian */
$(function() {
	$( "#accordion" ).accordion();
});

/* global variables */

var largeWidth = 960;
var smallWidth = 480;
var curWidth = $(window).width();
var hiddenSidebar = false;
var speedAmt = 1000;
var rightBarPixelAmt = "300px";

/* window resize event function */

var windowResize = function() {
	
	/* right side bar shows if enough width otherwise toggle */
	curWidth = $(window).width();
	if (curWidth < largeWidth) {
		$("#toggle").css("visibility", "visible");
		$(".right-sidebar-inner").css("border-left","1px solid black");
		$(".right-sidebar-inner").css("border-bottom","1px solid black");
		$(".right-sidebar-inner").hide("slide", {direction: "right"}, speedAmt);
		$(".post-content").css("margin-right", "0px");
		hiddenSidebar = true;
	}
	else {
		$("#toggle").css("visibility", "hidden");
		$(".right-sidebar-inner").css("border-left","none");
		$(".right-sidebar-inner").css("border-bottom","none");
		$(".right-sidebar-inner").show("slide", {direction: "right"}, speedAmt);
		$(".post-content").css("margin-right", rightBarPixelAmt);
		hiddenSidebar = false;
	}
};

/* toggle logic for side bar */
var toggleSidebar = function() {
	if (curWidth < largeWidth) {
		if (hiddenSidebar) {
			$(".right-sidebar-inner").show("slide", {direction: "right"}, speedAmt);
			$(".post-content").css("margin-right", "0px");
			hiddenSidebar = false;
		}
		else {
			$(".right-sidebar-inner").hide("slide", {direction: "right"}, speedAmt);
			$(".post-content").css("margin-right", "0px");
			hiddenSidebar = true;
		}
	}
	else {
		$(".right-sidebar-inner").show("slide", {direction: "right"}, speedAmt);
		$(".post-content").css("margin-right", rightBarPixelAmt);
		hiddenSidebar = false;
	}
};

$(window).resize(function() { windowResize() });

$(document).ready(function() {
	windowResize();
	$('#toggle').click(function () { toggleSidebar() });
});