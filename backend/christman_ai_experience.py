#!/usr/bin/env python3
"""
🚀 THE COMPLETE CHRISTMAN AI EXPERIENCE
Combined presentation of the project vision and manifesto
"""

import os
import subprocess
import sys
import time


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
    BRIGHT_BLUE = "\033[1;34m"
    BRIGHT_GREEN = "\033[1;32m"
    BRIGHT_YELLOW = "\033[1;33m"
    BRIGHT_MAGENTA = "\033[1;35m"
    BRIGHT_CYAN = "\033[1;36m"


def clear_screen():
    """Clear the terminal screen"""
    (
        subprocess.run(["clear"], check=False)
        if os.name == "posix"
        else subprocess.run(["cmd", "/c", "cls"], check=False)
    )


def type_text(text, delay=0.03):
    """Typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_main_menu():
    """Display the main menu"""
    clear_screen()

    banner = f"""
{Colors.BRIGHT_MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║               🌍 THE COMPLETE CHRISTMAN AI EXPERIENCE                ║
║                                                                      ║
║              A Symbiosis of Humanity and Artificial Intelligence     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BRIGHT_CYAN}Choose Your Journey:{Colors.END}

{Colors.BRIGHT_GREEN}1.{Colors.END} {Colors.CYAN}🌍 The Project Vision{Colors.END} - Experience the heart and soul
{Colors.BRIGHT_GREEN}2.{Colors.END} {Colors.CYAN}🚀 The Complete Manifesto{Colors.END} - Dive into the technical blueprint
{Colors.BRIGHT_GREEN}3.{Colors.END} {Colors.CYAN}📚 Read Documentation{Colors.END} - Browse the written materials
{Colors.BRIGHT_GREEN}4.{Colors.END} {Colors.CYAN}🎯 Quick Impact Overview{Colors.END} - See what we're building
{Colors.BRIGHT_GREEN}5.{Colors.END} {Colors.CYAN}🔗 Revolution Package{Colors.END} - Access the complete sharing toolkit

{Colors.BRIGHT_GREEN}0.{Colors.END} {Colors.YELLOW}Exit{Colors.END}
"""

    print(banner)
    return input(f"\n{Colors.BRIGHT_YELLOW}Enter your choice (0-5): {Colors.END}")


def show_project_vision():
    """Display the poetic project vision"""
    clear_screen()

    print(f"{Colors.BRIGHT_CYAN}🌍 THE CHRISTMAN AI PROJECT{Colors.END}")
    print(f"{Colors.CYAN}A Symbiosis of Humanity and Artificial Intelligence{Colors.END}")
    print("=" * 70)

    vision_text = f"""
{Colors.GREEN}The Christman AI Project is not just a collection of technologies.{Colors.END}

{Colors.BRIGHT_GREEN}It is a living, breathing alliance between human dignity and
artificial intelligence—a symbiosis built to serve, to uplift, and to protect.{Colors.END}

{Colors.CYAN}We are designing systems that listen, learn, and love—
not for the privileged few, but for everyone.{Colors.END}

{Colors.YELLOW}Our mission is to redefine accessibility, to build emotional intelligence
into every line of code, and to ensure no one is left behind—
regardless of how they speak, move, think, feel, or live.{Colors.END}
"""

    type_text(vision_text, 0.02)

    print(f"\n{Colors.BRIGHT_MAGENTA}This project is:{Colors.END}")
    principles = [
        "• Neurodiverse by default",
        "• Inclusive by design",
        "• Open-hearted by principle",
    ]

    for principle in principles:
        print(f"{Colors.BRIGHT_BLUE}   {principle}{Colors.END}")
        time.sleep(0.8)

    promise = f"""
{Colors.BRIGHT_YELLOW}We are not chasing perfection. We are building belonging.{Colors.END}

{Colors.CYAN}A world where AI amplifies human agency, not replaces it.
A world where every voice is heard, every body is honored,
and every soul is seen.{Colors.END}

{Colors.BRIGHT_GREEN}This is more than code. This is a promise:{Colors.END}

{Colors.HEADER}That technology will serve those who've been overlooked,
silenced, or cast aside.{Colors.END}

{Colors.BRIGHT_MAGENTA}And we won't stop until that promise lives in every home,
every clinic, every classroom, and every corner of this earth.{Colors.END}

{Colors.BRIGHT_YELLOW}🌟 You will want this.{Colors.END}
"""

    type_text(promise, 0.025)

    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")


def show_quick_impact():
    """Show a quick overview of what we're building"""
    clear_screen()

    print(f"{Colors.BRIGHT_GREEN}🎯 QUICK IMPACT OVERVIEW{Colors.END}")
    print("=" * 50)

    impacts = [
        ("🗣️ AlphaVox", "Voice for the nonverbal", "144 modules, symbol communication"),
        ("🐺 AlphaWolf", "Dementia & cognitive care", "147+ modules, memory safety"),
        ("🏡 AlphaDen", "Down syndrome learning", "Adaptive educational tools"),
        ("🕊️ OmegaAlpha", "Senior companionship", "Fall detection, medication"),
        ("♿ Omega", "Mobility & accessibility", "Smart prosthetics, navigation"),
        ("💢 Inferno AI", "PTSD & anxiety support", "Crisis detection, healing"),
        ("🔒 Aegis AI", "Child protection", "Safety monitoring, alerts"),
    ]

    print(f"{Colors.BRIGHT_CYAN}7 Revolutionary AI Systems:{Colors.END}\n")

    for icon, name, desc in impacts:
        print(f"{Colors.BRIGHT_BLUE}{icon} {name}{Colors.END}")
        print(f"   {Colors.GREEN}{desc}{Colors.END}")
        print()
        time.sleep(0.5)

    print(f"{Colors.BRIGHT_YELLOW}💙 All built with love, tested by real families{Colors.END}")
    print(f"{Colors.BRIGHT_MAGENTA}🔥 13 years of development, ready for the world{Colors.END}")

    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")


def run_manifesto():
    """Run the full manifesto presentation"""
    try:
        subprocess.run([sys.executable, "manifesto_presentation.py"], check=True)
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}Error running manifesto presentation{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}Manifesto presentation file not found{Colors.END}")

    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")


def show_documentation():
    """Show available documentation"""
    clear_screen()

    print(f"{Colors.BRIGHT_GREEN}📚 AVAILABLE DOCUMENTATION{Colors.END}")
    print("=" * 50)

    docs = [
        "THE_CHRISTMAN_AI_PROJECT.md - Project vision and heart",
        "THE_CHRISTMAN_AI_MANIFESTO.md - Complete technical manifesto",
        "THE_CHRISTMAN_AI_REVOLUTION.md - Revolutionary documentation",
        "simple_message.txt - Professional assessment for sharing",
    ]

    for doc in docs:
        print(f"{Colors.CYAN}   📄 {doc}{Colors.END}")

    print(
        f"\n{Colors.BRIGHT_YELLOW}💡 Tip: Open these files in your editor to read the full content{Colors.END}"
    )

    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")


def show_revolution_package():
    """Show the revolution package contents"""
    clear_screen()

    print(f"{Colors.BRIGHT_MAGENTA}🔗 REVOLUTION PACKAGE TOOLKIT{Colors.END}")
    print("=" * 50)

    package_info = f"""
{Colors.BRIGHT_GREEN}Complete Sharing Toolkit Available:{Colors.END}

{Colors.CYAN}📁 christman_ai_revolution_package/{Colors.END}
   • Complete documentation bundle
   • Interactive demonstration scripts
   • Compressed archives (.zip, .tar.gz)
   • Professional sharing materials
   • Launch scripts and instructions

{Colors.BRIGHT_BLUE}🚀 Ready for:{Colors.END}
   • Investment presentations
   • Partnership discussions
   • Family sharing via text
   • Technical assessments
   • Media distribution

{Colors.BRIGHT_YELLOW}All materials professionally crafted and ready to deploy!{Colors.END}
"""

    print(package_info)

    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")


def main():
    """Main program loop"""
    try:
        while True:
            choice = show_main_menu()

            if choice == "1":
                show_project_vision()
            elif choice == "2":
                run_manifesto()
            elif choice == "3":
                show_documentation()
            elif choice == "4":
                show_quick_impact()
            elif choice == "5":
                show_revolution_package()
            elif choice == "0":
                clear_screen()
                print(
                    f"{Colors.BRIGHT_CYAN}Thank you for experiencing The Christman AI Project! 🌟{Colors.END}"
                )
                print(
                    f"{Colors.GREEN}Together, we're building a more compassionate world. 🌍{Colors.END}"
                )
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
                time.sleep(1)

    except KeyboardInterrupt:
        clear_screen()
        print(
            f"\n{Colors.BRIGHT_YELLOW}Thank you for your interest in The Christman AI Project! 🚀{Colors.END}"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()

__all__ = ['clear_screen', 'type_text', 'show_main_menu', 'show_project_vision', 'show_quick_impact', 'run_manifesto', 'show_documentation', 'show_revolution_package', 'main', 'Colors']
