<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;


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

use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;

Route::post('/login',[AuthController::class,'login']);
Route::post('/register',[AuthController::class,'register']);
Route::post('/forgotpassword', [AuthController::class, 'forgotPassword']);
Route::post('/resetpassword', [AuthController::class, 'resetPassword']);
Route::middleware('auth:api')->group(function(){
    Route::post('/logout',[AuthController::class,'logout']);
    Route::get('/profile', [UserController::class, 'profile']); // Ver perfil propio
    Route::put('/profile', [UserController::class, 'updateProfile']); // Editar perfil propio
    Route::get('/',function(){
        return 3;
    });
});
Route::middleware('auth:api','role:admin')->group(function(){
    Route::get('/admin',function(){
        return 'Solo admin puede ver esto';
    });
    Route::get('/users', [UserController::class, 'index']); // Listar usuarios
    Route::post('/users', [UserController::class, 'store']); // Crear usuario
    Route::get('/users/{id}', [UserController::class, 'show']); // Ver usuario
    Route::put('/users/{id}', [UserController::class, 'update']); // Editar usuario
    Route::delete('/users/{id}', [UserController::class, 'destroy']); // Eliminar usuario
  
});
Route::middleware('auth:api','role:user')->group(function(){
    Route::get('/user',function(){
        return 'Solo user puede ver esto';
    });
   
});
