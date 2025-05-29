import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo'

// Query for cancelled shipments
export const getCancelledShipments = async () => {
  try {
    const { data } = await apolloClient.query({
      query: gql`
        query GetCancelledShipments {
          filteredData(filterInput: { 
            shipmentType: "Outgoing",
            shipmentStatus: "CANCELLED"
          }) {
            ... on ShipmentType {
              id
              date
              status
              location
              receiveDate
              entryTime
              weight1Time
              weight2Time
              exitTime
              licenseNumber
              customerName
              supplierName
              unloadLocation
              unit
              quantity
              quality
              penalty
              listOfReels
              profileName
              width
              salesId
              pricePerKg
              materialName
              invoiceStatus
              paymentStatus
              documentInfo
              comments
              cancellationReason
              username
              logs
            }
          }
        }
      `
    })
    return data?.filteredData || []
  } catch (error) {
    console.error('Error fetching cancelled shipments:', error)
    throw error
  }
}

// Query for cancelled purchases
export const getCancelledPurchases = async () => {
  try {
    const { data } = await apolloClient.query({
      query: gql`
        query GetCancelledPurchases {
          filteredData(filterInput: { 
            shipmentType: "Incoming",
            shipmentStatus: "CANCELLED"
          }) {
            ... on ShipmentType {
              id
              date
              status
              location
              receiveDate
              entryTime
              weight1Time
              weight2Time
              exitTime
              licenseNumber
              customerName
              supplierName
              unloadLocation
              unit
              quantity
              quality
              penalty
              listOfReels
              profileName
              width
              salesId
              pricePerKg
              materialName
              invoiceStatus
              paymentStatus
              documentInfo
              comments
              cancellationReason
              username
              logs
            }
          }
        }
      `
    })
    return data?.filteredData || []
  } catch (error) {
    console.error('Error fetching cancelled purchases:', error)
    throw error
  }
}

// Example usage:
/*
import { getCancelledShipments, getCancelledPurchases } from '@/components/testQueries'

// In your component:
async function testCancelledItems() {
  try {
    const cancelledShipments = await getCancelledShipments()
    console.log('Cancelled Shipments:', cancelledShipments)

    const cancelledPurchases = await getCancelledPurchases()
    console.log('Cancelled Purchases:', cancelledPurchases)
  } catch (error) {
    console.error('Test failed:', error)
  }
}
*/ 