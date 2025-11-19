<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class CheckAuthGateway
{
    public function handle(Request $request, Closure $next, ...$roles)
    {
        // 1. Verificar si viene el token
        $token = $request->header('Authorization');

        if (!$token) {
            return response()->json(['error' => 'Token requerido'], 401);
        }

        // 2. Validar token enviándolo al microservicio de seguridad
        $profileUrl = env('MS_SEGURIDAD') . '/api/profile';

        $response = Http::withHeaders([
            'Authorization' => $token
        ])->get($profileUrl);

        if ($response->status() != 200) {
            return response()->json(['error' => 'Token inválido'], 401);
        }

        $user = $response->json();

        // 3. Verificar rol si el endpoint lo requiere
        if (!empty($roles)) {
            if (!in_array($user['role_id'], $roles)) {
                return response()->json(['error' => 'No autorizado'], 403);
            }
        }

        // 4. Adjuntar info del usuario para el ProxyController si la necesitas
        $request->merge(['gateway_user' => $user]);

        return $next($request);
    }
}

