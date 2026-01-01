/** Middleware to protect routes requiring authentication. */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getSession(headers: Headers): Promise<{ user_id: string; email: string } | null> {
  const token = headers.get("authorization")?.replace("Bearer ", "");
  if (!token) return null;

  try {
    const response = await fetch(API_URL + "/auth/verify", {
      headers: { Authorization: "Bearer " + token },
    });
    if (response.ok) {
      return await response.json();
    }
  } catch {
    return null;
  }
  return null;
}

export async function authMiddleware(request: NextRequest) {
  // Check for session
  const session = await getSession(request.headers);

  // Define protected routes
  const protectedRoutes = ["/"];
  const authRoutes = ["/sign-in", "/sign-up"];

  const { pathname } = request.nextUrl;

  // If trying to access protected route without session, redirect to sign-in
  if (
    protectedRoutes.some((route) => pathname.startsWith(route)) &&
    !session
  ) {
    const signInUrl = new URL("/sign-in", request.url);
    signInUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(signInUrl);
  }

  // If authenticated user tries to access auth routes, redirect to home
  if (authRoutes.some((route) => pathname.startsWith(route)) && session) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
