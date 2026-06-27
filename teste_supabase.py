from database import supabase

try:
    resposta = supabase.table("materiais").select("*").execute()

    print("✅ Conectado ao Supabase!")
    print(resposta.data)

except Exception as e:
    print("❌ Erro:")
    print(type(e).__name__)
    print(e)