rm -f nohup.out
rm -rf faust_filter-data
nohup faust -A faust_filter worker -l info &
