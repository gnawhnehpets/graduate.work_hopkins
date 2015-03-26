/*
  ###################################################################
  ###This function executes our initial BLAST search via an AJAX call
  ###################################################################
*/
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#search_term').serialize();
    if(frmStr == 'search_term='){
	alert('Please enter in DNA or protein sequence in form');
    }else{
	alert('Please wait for BLAST results');
	$.ajax({
		url: './final.cgi',
		    dataType: 'json',
		    data: frmStr,
		    success: function(data, textStatus, jqXHR) {
		    processJSON(data);
		},
		    error: function(jqXHR, textStatus, errorThrown){
		    alert("Failed to perform BLAST search! textStatus: (" + textStatus +
			  ") and errorThrown: (" + errorThrown + ")");
		}
	    });
    }
}

/* 
   ####################################################################
   ###This processes a passed JSON structure representing BLAST results
   ###and draws it to the result table
   ####################################################################
*/
function processJSON( data ) {
    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    // set the span that lists the BLAST program used
    $('#program').text( data.program );
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
	    var this_row_id = 'result_row_' + next_row_num++;	    
        // create a row and append it to the body of the table
	    /*
	      $href->{'database'}=$db[$i];
	      $href->{'accession'}=$acc[$i];
	      $href->{'description'}=$desc[$i];
	      $href->{'score'}=$score[$i];
	      $href->{'evalue'}=$evalue[$i];
	     */
	    $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
	    //$('<td/>', { "text" : "checkbox" } ).appendTo('#' + this_row_id);
	    //	    $('<td/>', { "input type" : "checkbox" } ).appendTo('#' + this_row_id);
	    $('<td><input type="checkbox" name="items[]" value="' + this_row_id + '" /></td>').appendTo('#' + this_row_id);
	    //	    $('<td><input type="checkbox" /></td>').appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.database } ).appendTo('#' + this_row_id);	    
	    $('<td/>', { "text" : item.accession } ).appendTo('#' + this_row_id);	    
	    $('<td/>', { "text" : item.description } ).appendTo('#' + this_row_id); 
	    $('<td/>', { "text" : item.score } ).appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.evalue } ).appendTo('#' + this_row_id);
	});
    
    // now show the result section that was previously hidden
    $('#results').show();

}
/*
function refineResults{
    $('#results').hide();
}
*/
/*
  ############################################
  ###Run our javascript once the page is ready
  ############################################
*/

function getSelectedItems (){
    var selected = $('tbody tr').has(':checkbox:checked').map(function(index, el){
	    //td:eq('#') where # = number of row; 0=checkbox, 1=DB, 2=Accession, etc.
	    alert( $(this).find('td:eq(3)').text());	    
	})
	}

$(document).ready( function() {
	// define what should happen when a user clicks submit on our search form
	$('#submit').click( function() {
		runSearch();
		return false;  // prevents 'normal' form submission
	    });
	/*	$('#resubmit').click( function() {
                getSelectedItems();
                return false;  // prevents 'normal' form submission
            });
	*/
    });
