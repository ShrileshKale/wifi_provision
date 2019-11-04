
	$("#submit").click(function() {

		console.log("hii");
		var data = {
			"ssid" : $("#ssid").val(),
			"passwd" : $("#password").val()
		}

		console.log("Players");
		console.log(data);

		

		$.ajax({
			url: '/wifi/update_config',
			type: 'post',
			data: JSON.stringify(data),
			processData: false,
			dataType: 'json',
			success: function(response) {
				
				console.log("Inside Success");
				console.log(response);


			},
			failure: function(response) {
				console.log("Inside Failure");
				console.log(response);
				
			},
			error: function(response) {
				console.log("Inside Error");
				console.log(response);
				
			}
		});


	});



