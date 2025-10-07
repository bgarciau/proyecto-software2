<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class Role
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure(\Illuminate\Http\Request): (\Illuminate\Http\Response|\Illuminate\Http\RedirectResponse)  $next
     * @return \Illuminate\Http\Response|\Illuminate\Http\RedirectResponse
     */
public function handle($request, \Closure $next, $role = null)
{
    $user = auth()->user();

    if (!$user || !$user->role || $user->role->name !== $role) {
        return response()->json(['error' => 'No tienes permisos suficientes'], 403);
    }

    return $next($request);
}
}
