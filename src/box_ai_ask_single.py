from box_sdk_gen import AiItemBase, AiResponseFull, BoxClient, CreateAiAskMode

from utils.box_client_ccg import AppConfig, get_ccg_user_client
from utils.box_samples import files_start_with


def print_ai_response(prompt: str, ai_response: AiResponseFull):
    print()
    print("=" * 80)
    print(f"Prompt: {prompt}")
    print("-" * 80)
    print(f"Answer:\n{ai_response.answer}")
    print("=" * 80)
    print()


def main():
    conf = AppConfig()
    client: BoxClient = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    me = client.users.get_user_me()
    # cleat screen
    print("\033[H\033[J")
    print(f"Hello, I'm logged in as {me.name} ({me.id})")

    # find files starting with 'HAB-1' in Habitat Leases folder
    hab_files = files_start_with("HAB-1", client, conf)

    # AI Ask single Summarize document
    prompt = "Summarize document"
    item = AiItemBase(id=hab_files[0].id, type="file")
    ai_response: AiResponseFull = client.ai.create_ai_ask(
        mode=CreateAiAskMode.SINGLE_ITEM_QA,
        prompt=prompt,
        items=[item],
    )
    print_ai_response(prompt, ai_response)

    # Example prompts
    example_prompts = [
        "How many bedrooms does this unit has?",
        "When should I send a contract renewal notification?",
        "What is the annual rent for this unit?",
        "Can the tenant work from home?",
        "Are pets allowed?",
    ]

    # Infinite cycle to ask the user for prompts
    while True:
        # Display example prompts
        print("\nExample prompts:")
        for idx, example in enumerate(example_prompts, 1):
            print(f"{idx}. {example}")

        # Ask user for prompt or allow selection from examples
        prompt = input(
            f"\nEnter a prompt (or choose 1-{len(example_prompts)} from examples, 'q' to quit): "
        )

        if prompt == "q":
            break

        # Allow selection of example prompt if user chooses 1-5
        if prompt.isdigit() and 1 <= int(prompt) <= 5:
            prompt = example_prompts[int(prompt) - 1]

        # AI Ask single Summarize document
        item = AiItemBase(id=hab_files[0].id, type="file")
        ai_response: AiResponseFull = client.ai.create_ai_ask(
            mode=CreateAiAskMode.SINGLE_ITEM_QA,
            prompt=prompt,
            items=[item],
        )
        print_ai_response(prompt, ai_response)


if __name__ == "__main__":
    main()
