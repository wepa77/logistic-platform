export type UserType = 'shipper' | 'carrier'
export interface IUser {
  id: number
  username: string
  email: string
  phone?: string
  company_name?: string
  address?: string
  user_type: UserType
  verified: boolean
  balance?: string
  deposit_balance?: string
}
export interface IVehicle {
  id: number
  plate_number: string
  brand?: string
  model?: string
  year?: number
  capacity_kg: number
  volume_m3?: string
  truck_type?: string
  gps_enabled: boolean
  owner?: IUser
  owner_id?: number
  photo?: string
}
export interface ICargo {
  id: number
  title: string
  description?: string
  weight_kg: number
  volume_m3?: string
  pickup_address: string
  delivery_address: string
  pickup_date: string
  delivery_date?: string
  price_offer?: string
  status: 'open'|'in_progress'|'delivered'|'cancelled'
  created_at: string
  shipper?: IUser
  shipper_id?: number
  photo?: string
}
export interface IOffer {
  id: number
  price: string
  note?: string
  status: 'pending'|'accepted'|'rejected'
  created_at: string
  cargo: number | ICargo
  carrier?: IUser
  carrier_id?: number
  vehicle?: IVehicle
  vehicle_id?: number
}
export interface IShipment {
  id: number
  cargo: number | ICargo
  carrier?: IUser
  carrier_id?: number
  vehicle?: IVehicle
  vehicle_id?: number
  start_time: string
  end_time?: string
  total_price?: string
  distance_km?: string
  commission_amount: string
  payment_type: 'stripe'|'cash'|'bank'
  payment_status: 'pending'|'paid'|'failed'
  cash_received_by?: string
  received_date?: string
}
export interface IReview {
  id: number
  shipment: number | IShipment
  reviewer?: IUser
  reviewer_id?: number
  rating: number
  comment?: string
  created_at: string
}
export interface IWalletTx {
  id: number
  tx_type: 'top_up'|'commission'|'refund'|'deposit_top_up'|'deposit_commission'
  amount: string
  description?: string
  created_at: string
  success: boolean
}
export interface ITopUp {
  id: number
  amount: string
  stripe_session_id?: string
  created_at: string
  paid: boolean
}
