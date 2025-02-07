import click
from dotenv import load_dotenv
from core import direct_from_gemini, gemini_with_filtered_call_graph, clear_collection
from utils.db import create_table, get_state, get_all_state, insert_state
# Load environment variables from the .env file
load_dotenv()
create_table()

NOT_FIRST_RUN = 'not-first-run'
NO_EMBEDDINGS = 'NO_EMBEDDINGS'
EMBEDDING_EXISTS = 'embedding-exists'

def import_nltk_dependencies():
    import nltk
    nltk.download('punkt_tab')
    nltk.download("wordnet")
    
# Refresh deps
@click.command()
@click.option('--nltk', type=int, prompt="Should try fetching NLTK deps' latest version", help='1 True else False')
@click.option('--graph', prompt='Query to be asked about the JS code.', type=str, help='E.g. Add caching to verification call.')
def refresh(nltk_deps, call_graph):
    if nltk_deps == 1:
        import_nltk_dependencies()
    if call_graph == 1:
        clear_collection()
        insert_state(EMBEDDING_EXISTS, '0')
        

# Generate call graph and directly ask gemini
@click.command()
@click.option('--root', type=str, prompt='Root folder for JS project to create change plan for.', help='Absolute path D:/a/b/root')
@click.option('--query', prompt='Query to be asked about the JS code.', type=str, help='E.g. Add caching to verification call.')
@click.option('--direct', prompt='Directly send whole call graph to gemini without filtering', type=int, default=0, help='1 True else False')
@click.option('--embed', prompt='Parse code and embed to chroma', type=int, default=0, help='1 True else False')
def code(root, query, direct, embed):
    states = get_all_state()
    if NOT_FIRST_RUN not in states:
        click.echo(f'Downloading dependencies')
        import_nltk_dependencies()
    
    args = {'root': root, 'query': query, 'states': states, 'embed': embed }
    if direct == 1:
        direct_from_gemini(args)
    else:
        gemini_with_filtered_call_graph(args)

# Main CLI group
@click.group()
def cli():
    pass

cli.add_command(code)
cli.add_command(refresh)


if __name__ == '__main__':
    cli()