<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

use App\Models\User;
use Tymon\JWTAuth\Facades\JWTAuth;

use Illuminate\Support\Facades\Password;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $credentials = $request->only('email', 'password');

        if (!$token = JWTAuth::attempt($credentials)) {
            return response()->json(['error' => 'credenciales invalidas'], 401);
        }

        return response()->json([
            'token' => $token,
            'user' => Auth::user()
        ]);

    }
    public function register (Request $request)
    {
        $user = User::create([
            'name' => $request->input('name'),
            'email' => $request->input('email'),
            'password' => bcrypt($request->input('password')),
            'role_id' => 2 // Asigna el rol por defecto (2 = usuario normal
        ]);
        return response()->json([
            'message' => 'Usuario registrado exitosamente',
            'user' => $user]);
    }
    public function logout()
    {
        JWTAuth::invalidate(JWTAuth::getToken());
        return response()->json(['message' => 'Sesion cerrada exitosamente']);
    }

    public function forgotPassword(Request $request)
    {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        if ($status === Password::RESET_LINK_SENT) {
            return response()->json(['message' => 'Enlace de recuperación enviado al correo electrónico']);
        } else {
            return response()->json(['error' => 'No se pudo enviar el enlace de recuperación'], 400);
        }
    }

    public function resetPassword(Request $request)
{
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'token'),
        function ($user, $password) {
            $user->password = bcrypt($password);
            $user->save();
        }
    );

    if ($status === Password::PASSWORD_RESET) {
        return response()->json(['message' => 'Contraseña restablecida correctamente']);
    } else {
        return response()->json(['error' => 'Token inválido o expirado'], 400);
    }
}

}