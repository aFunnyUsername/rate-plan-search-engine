<html>
  <head>
    @include('includes.navbar')
  </head>
  <body>
    <div class="container" style="margin-top: 8%;">      
      <div class="col-md-6 offset-md-3 text-center">
        <div class="row">
          <div class="card" style="width: 100%;">
            <div class="card-header bg-dark text-white">Cheapest Plan: {{ $cheapest_plan['plan_description'] }}</div>
            <div class="card-body bg-light text-dark">
              <p>Supplier: {{ $cheapest_plan['supplier'] }} </p>
              <p>Fixed Price: {{ $cheapest_plan['pricing']['fixed_price'] }} </p> 
              <p>Variable Price: {{ $cheapest_plan['pricing']['variable_price'] }} </p>
              <p>Custom Price: {{ $cheapest_plan['pricing']['custom_price'] }} </p> 
              <p>Additional Fees: {{ $cheapest_plan['pricing']['additional_fees'] }} </p>
              <a href="#" class="btn btn-primary">Sign up for this Plan</a> 
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>











