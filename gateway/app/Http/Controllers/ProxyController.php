<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ProxyController extends Controller
{
    public function handle(Request $request, $service, $path = '')
    {
        $services = [
            'productos'     => env('MS_PRODUCTOS'),
            'reportes'      => env('MS_REPORTES'),
            'seguridad'     => env('MS_SEGURIDAD') . '/api',
            'usuarios'      => env('MS_USUARIOS') . '/api',
            'transacciones' => env('MS_TRANSACCIONES'),
        ];

        if (!isset($services[$service])) {
            return response()->json(['error' => 'Servicio no encontrado'], 404);
        }

        $base = rtrim($services[$service], '/');
        $path = ltrim($path ?? '', '/');

        $url = $path ? "$base/$path" : $base;


        // Petición al microservicio
        $response = Http::withHeaders($request->headers->all())
            ->send($request->method(), $url, [
                'query' => $request->query(),
                'json'  => $request->all(),
            ]);

        // Filtrar headers peligrosos
        $skip = [
            'transfer-encoding',
            'content-length',
            'content-encoding',
            'connection',
            'server',
            'date'
        ];

        $cleanHeaders = [];
        foreach ($response->headers() as $k => $v) {
            if (!in_array(strtolower($k), $skip)) {
                $cleanHeaders[$k] = $v;
            }
        }

        return response($response->body(), $response->status())
               ->withHeaders($cleanHeaders);
    }
}

