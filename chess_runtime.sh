# usage python process.py <actual_points [x, o]> <table state>
python game_theory/process.py 0 0 N N N N N X N N N N N N N N N N
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
  echo -e "\n" && read -n 1 -s -r -p "Press any key to continue..." && echo -e "\n"
fi
