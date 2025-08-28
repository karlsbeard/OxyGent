import { SocketProvider } from '@/shared/providers/SocketProvider';
import { Outlet } from '@modern-js/runtime/router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '@/styles/globals.css';

// Create a client with optimized defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
    mutations: {
      retry: 1,
    },
  },
});

export default function Layout() {
  return (
    <QueryClientProvider client={queryClient}>
      <SocketProvider>
        <div className="min-h-screen bg-gray-50">
          <Outlet />
        </div>
      </SocketProvider>
    </QueryClientProvider>
  );
}
