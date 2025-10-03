<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\AuthController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
// Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//     return $request->user();
// });

Route::post('/login',[AuthController::class,'login']);
Route::post('/register',[AuthController::class,'register']);
Route::post('/forgotpassword', [AuthController::class, 'forgotPassword']);
Route::post('/resetpassword', [AuthController::class, 'resetPassword']);
Route::middleware('auth:api')->group(function(){
    Route::post('/logout',[AuthController::class,'logout']);
    Route::get('/',function(){
        return 3;
    });
});
Route::middleware('auth:api','role:admin')->group(function(){
    Route::get('/admin',function(){
        return 'Solo admin puede ver esto';
    });
});
Route::middleware('auth:api','role:user')->group(function(){
    Route::get('/user',function(){
        return 'Solo user puede ver esto';
    });
});
