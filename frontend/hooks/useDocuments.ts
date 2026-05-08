import { useMutation, useQuery, useQueryClient } from "react-query"
import toast from "react-hot-toast"
import { apiClient } from "@/lib/api"
import { Document, UploadProgress } from "@/types"

/**
 * Custom hooks for document management
 * Handles all document-related operations with React Query
 */

/**
 * Fetch all documents
 */
export function useDocuments(page: number = 1, pageSize: number = 10) {
  return useQuery(
    ["documents", page, pageSize],
    () => apiClient.listDocuments(page, pageSize),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  )
}

/**
 * Fetch a single document
 */
export function useDocument(documentId: string) {
  return useQuery(
    ["document", documentId],
    () => apiClient.getDocument(documentId),
    {
      enabled: !!documentId,
      staleTime: 5 * 60 * 1000,
    }
  )
}

/**
 * Upload a document with progress tracking
 */
export function useUploadDocument() {
  const queryClient = useQueryClient()

  return useMutation(
    async (file: File) => {
      return apiClient.upload(file, (progress) => {
        // Could emit progress updates here
      })
    },
    {
      onSuccess: () => {
        toast.success("Document uploaded successfully")
        queryClient.invalidateQueries("documents")
      },
      onError: (error: any) => {
        const message =
          error?.response?.data?.message || "Failed to upload document"
        toast.error(message)
      },
    }
  )
}

/**
 * Delete a document
 */
export function useDeleteDocument() {
  const queryClient = useQueryClient()

  return useMutation(
    async (documentId: string) => {
      return apiClient.deleteDocument(documentId)
    },
    {
      onSuccess: () => {
        toast.success("Document deleted successfully")
        queryClient.invalidateQueries("documents")
      },
      onError: (error: any) => {
        const message =
          error?.response?.data?.message || "Failed to delete document"
        toast.error(message)
      },
    }
  )
}

/**
 * Reindex a document (regenerate embeddings)
 */
export function useReindexDocument() {
  const queryClient = useQueryClient()

  return useMutation(
    async (documentId: string) => {
      return apiClient.reindexDocument(documentId)
    },
    {
      onSuccess: () => {
        toast.success("Document reindexed successfully")
        queryClient.invalidateQueries("documents")
      },
      onError: (error: any) => {
        const message =
          error?.response?.data?.message || "Failed to reindex document"
        toast.error(message)
      },
    }
  )
}

/**
 * Search documents
 */
export function useSearch() {
  return useMutation(
    async (params: { query: string; documentIds?: string[]; topK?: number }) => {
      return apiClient.search({
        query: params.query,
        documentIds: params.documentIds,
        topK: params.topK,
      })
    },
    {
      onError: (error: any) => {
        const message =
          error?.response?.data?.message || "Search failed"
        toast.error(message)
      },
    }
  )
}
