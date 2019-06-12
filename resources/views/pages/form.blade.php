<!DOCTYPE html>
<html>
  <head>
    @include('includes.navbar')
  </head>
  <body>
    <div class="container" style="margin-top: 8%;">      
      <div class="col-md-6 offset-md-3 text-center">
        <div class="row">
          <div id="logo" class="text-center">
            <h1>Plug-in to Distributed Energy!</h1>
            <p>Search for the Cheapest Rate Plan</p>
          </div>
          <form role="form" id="form-buscar" class="form-inline justify-content-center" style="margin: 0 auto; width:100%;">
            <div class="form-group">
              <div class="input-group">
                <input id="1" class="form-control" type="text" name="search" placeholder="Search..." required/>
                <span class="input-group-btn">
                  <button class="btn btn-dark" type="submit">
                    <i class="glyphicon glyphicon-search" aria-hiden="true"></i> Search
                  </button>
                </span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
