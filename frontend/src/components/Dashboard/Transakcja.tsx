export default interface Transakcja {
  transaction_id: number;
  user_id: number;
  category_id: number | null;
  transaction_type: 'income' | 'expense';
  title: string;
  description: string | null;
  amount: number;
  transaction_method: string;
  account: string | null;
  account_owner: string | null;
  transaction_date: string;
}