<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use App\Http\Controllers\ProxyController;

// 🔥 Ruta explícita para el gateway
Route::any('/{service}/{path?}', [ProxyController::class, 'handle'])
    ->where([
        'service' => 'productos|reportes|seguridad|usuarios|transacciones',
        'path' => '.*'
    ]);

// 🔥 Fallback FINAL – si no coincide nada, error JSON
Route::fallback(function () {
    return response()->json(['error' => 'Ruta no encontrada en el gateway'], 404);
});

