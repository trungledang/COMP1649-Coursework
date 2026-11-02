const fs=require('fs'),vm=require('vm'); let page;
vm.runInNewContext(fs.readFileSync(process.argv[2],'utf8'),{$axure:{loadCurrentPage:p=>page=p}});
console.log(JSON.stringify(page.page.interactionMap,null,2));
