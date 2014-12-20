
//To add scheme 
$("#add_btn").live('click',function(e){
	e.preventDefault();
	var scheme_url = $("#scheme_url").val().trim();
	var scheme_name = $("#scheme_name").val().trim();
	var funding = $("#funding").val().trim();
	var benefits =$("#benefits").val().trim();
	var target =$("#target").val().trim();
	var department =$("#department").val().trim();
	var initiation =$("#initiation").val().trim();
	var objectives =$("#objectives").val().trim();
	var eligibility =$("#eligibility").val().trim();
	var documents =$("#documents").val().trim();
	var to_update = $("#to_update").val();
	if (to_update != 'undefined' ){
		to_update_id = to_update
	}

	var url = '/api/add_scheme';
	if(scheme_url != '' || scheme_name != '' || funding != '' || benefits !='' || target !='' || department !='' 
		|| initiation != '' || objectives != '' || eligibility != '' || documents != ''){
		if (to_update_id){
			var jsonData = JSON.stringify({'scheme_url': scheme_url, 'scheme_name': scheme_name,'funding':funding,
			'benefits':benefits,'target':target,'department':department,'coverage':initiation,
		     'objectives':objectives,'eligibility':eligibility,'documents':documents,'to_update_id':to_update_id});
		}
		else{
		var jsonData = JSON.stringify({'scheme_url': scheme_url, 'scheme_name': scheme_name,'funding':funding,
			'benefits':benefits,'target':target,'department':department,'coverage':initiation,
		     'objectives':objectives,'eligibility':eligibility,'documents':documents});
	}
		var params = {'jsonData':jsonData} 
		return $.post(url, params).then(function(res){ 
					if(res.success){
						smoke.confirm('Your thinsdfdvfdvf', function(e){
							if (e){
							window.location.href="/";
						}
					
						});
	}
});
 
 }
});

$("#cancel_btn").live('click',function(e){
	e.preventDefault();
	window.location.href = "/";
});