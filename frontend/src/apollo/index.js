import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { onError } from '@apollo/client/link/error'

// Error handling link
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      )
    )
  if (networkError) console.error(`[Network error]: ${networkError}`)
})

// HTTP connection to the API
const httpLink = createHttpLink({
  uri: 'http://localhost:8000/myapp/filter/graphql/',
  credentials: 'omit',  // Don't send credentials
  headers: {
    'Content-Type': 'application/json',
  }
})

// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: errorLink.concat(httpLink),
  cache,
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all',
    },
    query: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all',
    },
  }
})

export function setupApollo(app) {
  app.provide(DefaultApolloClient, apolloClient)
} 