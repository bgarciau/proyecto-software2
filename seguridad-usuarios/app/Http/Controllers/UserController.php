<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Tymon\JWTAuth\Facades\JWTAuth;

class UserController extends Controller
{
      // Listar todos los usuarios (solo admin)
    public function index()
    {
        return response()->json(User::all());
    }

    // Crear usuario (solo admin)
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|string',
            'email' => 'required|email|unique:users',
            'password' => 'required|string',
            'role_id' => 'required|integer'
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => bcrypt($request->password),
            'role_id' => $request->role_id
        ]);

        return response()->json(['message' => 'Usuario creado', 'user' => $user]);
    }

    // Ver usuario por ID (solo admin)
    public function show($id)
    {
        $user = User::find($id);
        if (!$user) {
            return response()->json(['error' => 'Usuario no encontrado'], 404);
        }
        return response()->json($user);
    }

    // Editar usuario por ID (solo admin)
    public function update(Request $request, $id)
    {
        $user = User::find($id);
        if (!$user) {
            return response()->json(['error' => 'Usuario no encontrado'], 404);
        }

        $user->update($request->only(['name', 'email', 'role_id']));
        if ($request->filled('password')) {
            $user->password = bcrypt($request->password);
            $user->save();
        }

        return response()->json(['message' => 'Usuario actualizado', 'user' => $user]);
    }

    // Eliminar usuario por ID (solo admin)
    public function destroy($id)
    {
        $user = User::find($id);
        if (!$user) {
            return response()->json(['error' => 'Usuario no encontrado'], 404);
        }
        $user->delete();
        return response()->json(['message' => 'Usuario eliminado']);
    }

    // Ver perfil propio
    public function profile()
    {
        return response()->json(Auth::user());
    }

    // Editar perfil propio
    public function updateProfile(Request $request)
    {
        $user = Auth::user();
        $user->update($request->only(['name', 'email']));
        if ($request->filled('password')) {
            $user->password = bcrypt($request->password);
            $user->save();
        }
        return response()->json(['message' => 'Perfil actualizado', 'user' => $user]);
    }
}
