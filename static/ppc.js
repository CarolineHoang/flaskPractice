
// Author: Caroline Hoang
// Two Lists that have Drag and Drop functionality between them: The Office Edition
// This version has a Flask Server to save changes
// [A UI Design Class Assignment]

// the lists we work with
var non_ppc_li = []; 
var ppc_li = [];


//this function displays the list after setting the lists to be equal to the updated server list
var display_lists = function(non_ppc, ppc){
    non_ppc_li = non_ppc;
    ppc_li =ppc;
    makeView();
} 

var draggableSettings= { //the settings with which we configure every draggable (name)
    cursor: 'move',    //make the name keep the move arrow while dragging
    revert: "invalid", //true
    stack: ".names"
  }

//make the divs for each name in the non-ppc list and give them data of their name and index
function makeNONListViews(){
    $('#non-ppc-list').empty();
    non_ppc_li.forEach(function(name, index){
        ($("<div class='names non-ppc'>" +index+": " + name + "</div>").data( 'name', name ).data( 'index', index )).draggable(draggableSettings).appendTo($('#non-ppc-list'));
    });
}

//make the divs for each name in the ppc list
function makeListViews(){
    $('#ppc-list').empty();
    ppc_li.forEach(function(name, index){
        ($("<div class='names ppc'>" +index+": " + name + "</div>").data( 'name', name ).data( 'index', index )).draggable(draggableSettings).appendTo($('#ppc-list'));
    });
}

//a function to run both of the above programs at once
function makeView(){
    makeNONListViews();
    makeListViews();
}

//this function updates the model on the server to add a dragged name to ppc and remove it from non-ppc
var move_to_ppc = function(name){
    var data_to_save = {"name": name}  
    $.ajax({
        type: "POST",
        url: "add_PPC_name",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),
        success: function(result){
            var nPPC_returned = result["nPPC_data"]
            var PPC_returned = result["PPC_data"]
            non_ppc_li = nPPC_returned;
            ppc_li = PPC_returned;
            display_lists(non_ppc_li, ppc_li )
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });

} 

//this function updates the model on the server to add a dragged name to non-ppc and remove it from ppc
var move_to_non_ppc = function(name){
    var data_to_save = {"name": name}       
    $.ajax({
        type: "POST",
        url: "add_nPPC_name",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),
        success: function(result){
            var nPPC_returned = result["nPPC_data"]
            var PPC_returned = result["PPC_data"]
            non_ppc_li = nPPC_returned;
            ppc_li = PPC_returned;
            display_lists(non_ppc_li, ppc_li )
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
} 

//main function
$(document).ready(function(){
    display_lists(nPPC_data, PPC_data);
    makeView();   //make the view on load

    //determine the behavior of the ppc droppable area while name is being dragged and on drop
    $('#ppc-list-target').droppable( {
        accept: ".non-ppc",
        tolerance: "touch", //accept any amount of overlay to make the drop off more sensitive
        //hoverClass is depreciated so I use classes instead
        classes: {
            "ui-droppable-active": "targeting", //make medium blue when dragging
            "ui-droppable-hover": "targeted"    //make dark blue when hovering above the drop off area
          },
        drop: function(event, ui){
            var new_name = $( ui.draggable ).data("name");
            move_to_ppc(new_name);
        }
      }); 
      $('#non-ppc-list-target').droppable( {
        accept: ".ppc",
        tolerance: "touch",
        classes: {
            "ui-droppable-active": "targeting",
            "ui-droppable-hover": "targeted"
          },
        drop: function(event, ui){
            var new_name = $( ui.draggable ).data("name");
            move_to_non_ppc(new_name);
        }
      });       
})





