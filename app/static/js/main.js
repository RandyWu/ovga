	$(document).ready(function(){
		$('#datepicker').datepicker({format: 'yyyy-mm-dd', todayHighlight: 'True'});
			$('#datepicker').on('changeDate', function() {
				$('#my_hidden_input').val( $('#datepicker').datepicker('getFormattedDate') );
		});
	});
	
	$(document).ready(function() {
		$(".main-table").clone(true).appendTo('#table-scroll').addClass('clone');   
  });
