<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use App\Http\Controllers\ProxyController;

// // 🔥 Ruta explícita para el gateway
// Route::any('/{service}/{path?}', [ProxyController::class, 'handle'])
//     ->where([
//         'service' => 'productos|reportes|seguridad|usuarios|transacciones',
//         'path' => '.*'
//     ]);

// // 🔥 Fallback FINAL – si no coincide nada, error JSON
// Route::fallback(function () {
//     return response()->json(['error' => 'Ruta no encontrada en el gateway'], 404);
// });


/*
|--------------------------------------------------------------------------
| RUTAS PÚBLICAS (NO REQUIEREN TOKEN)
|--------------------------------------------------------------------------
*/

// LOGIN
Route::post('/seguridad/login', function (Request $request) {
    return app(ProxyController::class)->handle($request, 'seguridad', 'login');
});

// REGISTER
Route::post('/seguridad/register', function (Request $request) {
    return app(ProxyController::class)->handle($request, 'seguridad', 'register');
});

// FORGOT PASSWORD
Route::post('/seguridad/forgotpassword', function (Request $request) {
    return app(ProxyController::class)->handle($request, 'seguridad', 'forgotpassword');
});

// RESET PASSWORD
Route::post('/seguridad/resetpassword', function (Request $request) {
    return app(ProxyController::class)->handle($request, 'seguridad', 'resetpassword');
});



/*
|--------------------------------------------------------------------------
| RUTAS DE SEGURIDAD (TOKEN OBLIGATORIO)
|--------------------------------------------------------------------------
*/

Route::middleware('gatewayauth')->group(function () {

    Route::post('/seguridad/logout', function (Request $request) {
        return app(ProxyController::class)->handle($request, 'seguridad', 'logout');
    });

    Route::get('/seguridad/profile', function (Request $request) {
        return app(ProxyController::class)->handle($request, 'seguridad', 'profile');
    });

});



/*
|--------------------------------------------------------------------------
| RUTAS DE USUARIOS – SOLO ADMIN (role_id = 1)
|--------------------------------------------------------------------------
*/

Route::middleware('gatewayauth:1')->group(function () {

    Route::any('/usuarios/{path?}', function (Request $request, $path = null) {
        return app(ProxyController::class)->handle($request, 'usuarios', $path);
    })->where('path', '.*');

});



/*
|--------------------------------------------------------------------------
| RUTAS GENERALES (TOKEN OBLIGATORIO)
|--------------------------------------------------------------------------
*/

Route::middleware('gatewayauth')->group(function () {

    // Productos
    Route::any('/productos/{path?}', function (Request $request, $path = null) {
        return app(ProxyController::class)->handle($request, 'productos', $path);
    })->where('path', '.*');


    // Transacciones
    Route::any('/transacciones/{path?}', function (Request $request, $path = null) {
        return app(ProxyController::class)->handle($request, 'transacciones', $path);
    })->where('path', '.*');


    // Reportes
    Route::any('/reportes/{path?}', function (Request $request, $path = null) {
        return app(ProxyController::class)->handle($request, 'reportes', $path);
    })->where('path', '.*');

});



/*
|--------------------------------------------------------------------------
| Fallback Global
|--------------------------------------------------------------------------
*/

Route::fallback(function () {
    return response()->json(['error' => 'Ruta no encontrada en el gateway'], 404);
});
