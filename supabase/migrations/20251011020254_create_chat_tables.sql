-- Table for storing chat completions
DROP TABLE IF EXISTS public.ai_usage;
CREATE TABLE public.ai_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  cost NUMERIC NOT NULL,
  usage JSONB DEFAULT '{}',
  metadata JSONB DEFAULT '{}',
  created_at timestamp default now(),
  updated_at timestamp default now()
);

-- Enable RLS
ALTER TABLE public.ai_usage ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view own ai usage" ON public.ai_usage;
DROP POLICY IF EXISTS "Users can insert own ai usage" ON public.ai_usage;
DROP POLICY IF EXISTS "Users can update own ai usage" ON public.ai_usage;

-- Create new policies that work better with upsert
CREATE POLICY "Users can view own ai usage" ON public.ai_usage
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own ai usage" ON public.ai_usage
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own ai usage" ON public.ai_usage
  FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Also create a policy for DELETE if needed
CREATE POLICY "Users can delete own ai usage" ON public.ai_usage
  FOR DELETE USING (auth.uid() = user_id);
