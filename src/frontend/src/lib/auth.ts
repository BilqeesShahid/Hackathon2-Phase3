export const auth = {
  api: {
    getSession: async () => {
      const token = localStorage.getItem("auth_token");
      if (!token) return { session: null };
      try {
        const response = await fetch(process.env.NEXT_PUBLIC_API_URL + "/auth/verify", {
          headers: { Authorization: "Bearer " + token },
        });
        if (response.ok) {
          const result = await response.json();
          return { session: { user: { id: result.user_id, email: result.email, name: null, image: null }, token } };
        }
      } catch (e) {
        console.error("getSession error:", e);
      }
      return { session: null };
    },
  },
};
