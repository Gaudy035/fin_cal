export default interface TPowtarzalna {
  recurring_id: number;
  user_id: number;
  category_id: number | null;
  transaction_type: 'income' | 'expense';
  title: string;
  description: string | null;
  amount: number;
  transaction_method: string;
  account: string | null;
  account_owner: string | null;
  next_date: string;
  interval: string;
  is_active: boolean | number;
}