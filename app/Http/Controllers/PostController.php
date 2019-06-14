<?php

namespace App\Http\Controllers;

use DB;
use Illuminate\Http\Request;
use App\Post;

class PostController extends Controller
{
  public function search(){
    return view('pages.search');
  }
  
  public function send(Request $request){
    //dd($request->zipcode);
    $zones = [
      'ameren I' => 'Ameren Illinois Rate Zone I',
      'ameren II' => 'Ameren Illinois Rate Zone II',
      'ameren III' => 'Ameren Illinois Rate Zone III',
      'comed' => 'ComEd',
      'midamerican' => 'MidAmerican',];
      
    $data = new Post($request->all());
    $zipcode = $data['search'];
    $rate_zone = $zones[$zipcode];

    $plans = DB::collection($rate_zone)->get();
    
    $cheapest_plan = null;
    
    foreach($plans as $plan)
    {
      if (is_null($cheapest_plan))
      {
        $cheapest_plan = $plan;
      }

      $pricing = $plan['pricing'];
      $fixed_price = $pricing['fixed_price'];

      if (!is_null($fixed_price) and $fixed_price != 0)
      {
        if ($fixed_price < $cheapest_plan['pricing']['fixed_price'])
        {
          $cheapest_plan = $plan;
        }
      }
    }
    return view('pages.result', compact('cheapest_plan'));
  }
}
