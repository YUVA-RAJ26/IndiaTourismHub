$(document).ready(function() {
    // Populate states dropdown
    $.ajax({
      url: '/admin-module/states/',  // Replace with the actual API endpoint for fetching states
      method: 'GET',
      success: function(data) {
        var states = data.results;
        var stateSelect = $('#state');

        // Iterate over states and append options to the dropdown
        states.forEach(function(state) {
          stateSelect.append('<option value="' + state.id + '">' + state.name + '</option>');
        });
        
        // Trigger change event to load districts based on initial state selection
        stateSelect.trigger('change');
      },
      error: function(xhr, textStatus, errorThrown) {
        console.error('Failed to fetch states:', errorThrown);
      }
    });
  
    // Populate districts based on selected state
    $('#state').on('change', function() {
      var stateId = $(this).val();
      var districtSelect = $('#district');
      
      // Clear previous options
      districtSelect.empty();
      
      // Fetch districts based on stateId
      $.ajax({
        url: '/admin-module/districts/get_state_districts/' + stateId + '/',
        method: 'GET',
        success: function(data) {
          var districts = data;
          
          // Iterate over districts and append options to the dropdown
          districts.forEach(function(district) {
            districtSelect.append('<option value="' + district.id + '">' + district.name + '</option>');
          });
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error('Failed to fetch districts:', errorThrown);
        }
      });
    });
  
    // Auto-select state and district based on pincode
    $('#pincode').on('blur', function() {
        var pincode = $(this).val();
        
        // Fetch state and district based on pincode
        $.ajax({
          url: '/admin-module/districts/get_pincode_state_districts/',
          data: { pincode: pincode }, 
          method: 'GET',
          success: function(data) {
            if (data.length > 0) {
              var stateId = data[0].state_id;
              var districtName = data[0].name;
              
              // Set selected state and district in the dropdowns
              $('#state').val(stateId).trigger('change');
              $('#district').val(districtName).trigger('change');
            } else {
              $('#state').val('').trigger('change');
              $('#district').val('').trigger('change');
              alert('Pincode not found');
            }
          },
          error: function(xhr, textStatus, errorThrown) {
            console.error('Failed to fetch state and district based on pincode:', errorThrown);
          }
        });
    });
      

});
  