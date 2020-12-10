var path = Server.path;

// 选择的时候调用的方法
$('#file_tree').on("changed.jstree", function (e, data) {
	var path = $('#file_tree').jstree().get_path(data.selected);
	if (path) {
		path = path.join('/');
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				eval("pathinfo="+this.responseText);

				//右侧表格信息
				document.getElementById('info_table').innerHTML = '<tr><th colspan="2">' + pathinfo.name + '</th></tr><tr>&nbsp;</tr>'

				if (pathinfo.isfile) {//是文件

					document.getElementById('info_table').innerHTML += '<tr><td>文件</td></tr><tr>&nbsp;</tr>'
					document.getElementById('info_table').innerHTML += '<tr><td>大小：</td><td>' + pathinfo.size + '</td></tr>'
					document.getElementById('info_table').innerHTML += '<tr><td>创建时间：</td><td>' + pathinfo.ctime + '</td></tr>'
					document.getElementById('info_table').innerHTML += '<tr><td>MIME类型：</td><td>' + pathinfo.MIME + '</td></tr>'
					document.getElementById('info_table').innerHTML += '<tr><td colspan="2"><a href="'+pathinfo.url+'">下载</a></td><td>'
					
					//预览
					if (pathinfo['MIME'] == "image/jpeg") {
						document.getElementById('file_show').innerHTML = '<img style="position:absolute; width:auto; height:auto; max-width:100%; max-height:100%" src="'+pathinfo.url+'"&alt="'+pathinfo.name+'" />';
					}
					else if (pathinfo['MIME'] == "image/png") {
						document.getElementById('file_show').innerHTML = '<img style="position:absolute; width:auto; height:auto; max-width:100%; max-height:100%" src="'+pathinfo.url+'"&alt="'+pathinfo.name+'" />';
					}
					else if (pathinfo['MIME'] == "video/mp4") {
						document.getElementById('file_show').innerHTML = '\
							<video style="position:absolute; width:100%; height:100%; max-width:100%; max-height:100%" id="video" class="video-js vjs-default-skin" controls preload="none">\
							<source src="'+pathinfo.url+'"&alt="'+pathinfo.name+'" type="video/mp4">\
							</video>\
							<style type="text/css">\
							.video-js{width:auto; height:auto; max-width:100%; max-height:100%}\
							</style>';
					}
					else {
						document.getElementById('file_show').innerHTML = '<p>此文件无法预览</p>'
					}
				} else {//是文件夹
					document.getElementById('info_table').innerHTML += '<tr><td>文件夹</td></tr><tr>&nbsp;</tr>'
					document.getElementById('info_table').innerHTML += '<tr><td>创建时间：</td><td>' + pathinfo.ctime + '</td></tr>'

				}
			}
		}
		xhttp.open("GET", "/file/pathinfo?path="+path+'&t='+ Math.random(), true);
		xhttp.send();
	}
});

//一般data从后台返回，调用这个方法显示视图
$('#file_tree').jstree({
		'plugins':["search","themes","types","state","line"],	 //包含样式，选择框，图片等	
		'types': {
			'default': {
				'icon': true // 默认图标,可以写路径名，但是必须将themes的icons打开，否则没有地方展示图标
			},
	   },
		
		
		"checkbox":{  // 去除checkbox插件的默认效果
			tie_selection : true,
			keep_selected_style : true,
			whole_node : true
		},
	   
		'core' : {	//core主要功能是控制树的形状，单选多选等等
			'data' :{	//填充数据,data需要识别格式,关键字为id, text,children,展示时显示的是text,传递的可以是id也可以是text
				"url" : "/file/filetree?path=" + path + '&t=' + Math.random(),
				"dataType" : "json",
			},		 
			'themes':{
				"icons":true,	//默认图标
				"theme": "classic",
				"dots": true,
				"stripes" : true,	//增加条纹
			},	//关闭文件夹样式
			'dblclick_toggle': true,   //允许tree的双击展开,默认是true
			"multiple" : false, // 单选
			"check_callback" : true
		} 
	}
)

// 搜索功能的方法 file_tree：数据展示的内容	plugins4_q 搜索框
var to = false;
$('#plugins4_q').keyup(function () {
	if(to) { clearTimeout(to); }
		to = setTimeout(function () {
		  var v = $('#plugins4_q').val();
		  $('#file_tree').jstree(true).search(v);
	}, 250);
});
