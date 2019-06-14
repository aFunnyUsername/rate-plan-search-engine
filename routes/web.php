<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('pages.welcome');
});


Route::get('/search', 'PostController@search')->name('pages.search');
Route::post('/search/send', 'PostController@send')->name('pages.send');

//Route:get('/result', 'PostController@show_result')->name('pages.result');

