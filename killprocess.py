import psutil
import argparse
import sys
def main():
    # breakpoint()
    parser = argparse.ArgumentParser(description="Kill Process")
    parser.add_argument('-pid', '--pid', type=str,help="pid")
    args = parser.parse_args()

    if not args.pid:
        sys.exit()
    proc = psutil.Process(int(args.pid))
    proc.terminate() 
if __name__ == '__main__':
    main()