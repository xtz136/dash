webpackJsonp([1],{"+skl":function(t,e){},"30Op":function(t,e){},"7dH6":function(t,e){},HpQW:function(t,e){},JPGY:function(t,e){},NHnr:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n("7+uW"),a={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"layout"},[n("Layout",[n("Header",[n("Menu",{attrs:{mode:"horizontal",theme:"dark","active-name":"1"}},[n("img",{staticClass:"layout-logo",attrs:{src:t.$store.state.config.logoImg}}),t._v(" "),n("div",{staticClass:"layout-company-name"},[t._v(t._s(t.$store.state.config.companyName))]),t._v(" "),n("div",{staticClass:"layout-nav"},[n("MenuItem",{attrs:{name:"1"}},[n("Icon",{attrs:{type:"ios-navigate"}}),t._v(" "),n("router-link",{attrs:{to:"/company"}},[t._v("资料录入")])],1),t._v(" "),n("MenuItem",{attrs:{name:"2"}},[n("Icon",{attrs:{type:"ios-navigate"}}),t._v(" "),n("router-link",{attrs:{to:"/revertentitys"}},[t._v("资料归还单")])],1),t._v(" "),n("MenuItem",{attrs:{name:"3"}},[n("Icon",{attrs:{type:"ios-keypad"}}),t._v(" "),n("a",{attrs:{target:"_blank",href:t.$store.state.config.adminUrl}},[t._v("管理后台")])],1)],1)])],1),t._v(" "),n("router-view"),t._v(" "),n("Footer",{staticClass:"layout-footer-center"},[t._v("2018 © "+t._s(t.$store.state.config.companyName))])],1)],1)},staticRenderFns:[]};var r=n("VU/8")({computed:{}},a,!1,function(t){n("gz2f"),n("HpQW")},"data-v-23119d82",null).exports,s=n("/ocq"),o=n("Dd8w"),c=n.n(o),d={name:"ListCompany",data:function(){var t=this;return{searchValue:"",loading:!0,columns:[{type:"index",align:"center",width:60},{title:"标题",key:"title",width:200},{title:"所属行业",key:"industry"},{title:"业务员",key:"saleman"},{title:"记账会计",key:"bookkeeper"},{title:"纳税人类型",key:"taxpayer_type"},{title:"执照过期日期",key:"license_status"},{title:"代理状态",key:"status"},{title:"联系人信息",key:"contactor_info",width:200},{title:"操作",key:"action",align:"center",render:function(e,n){return e("div",[e("Button",{props:{type:"primary",size:"small"},style:"margin-bottom: 5px",on:{click:function(){t.toListEntity(n.row.id)}}},"资料管理")])}}]}},methods:{toListEntity:function(t){this.$router.push({name:"ListEntity",params:{companyId:t}})},toListRevertEntity:function(t){this.$router.push({name:"ListRevertEntity",params:{companyId:t}})},pageChange:function(t){var e=this,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};this.$store.dispatch("FETCH_COMPANY_LIST",c()({page:t},n)).then(function(n){e.$store.commit("SET_PAGINATION_PAGE",t),e.$store.commit("SET_PAGINATION_COUNT",n.msg.count),e.loading=!1})},search:function(t){13===t.which&&(this.loading=!0,this.pageChange(1,{title:this.searchValue}))}},computed:{pagination:function(){return this.$store.state.pagination.data},data:function(){return this.$store.getters.companyList}},created:function(){window.title=this.$store.state.config.companyName,this.pageChange(this.pagination.page)}},l={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Input",{attrs:{placeholder:"搜索公司",icon:"ios-search"},on:{"on-keypress":t.search},model:{value:t.searchValue,callback:function(e){t.searchValue=e},expression:"searchValue"}}),t._v(" "),n("Table",{attrs:{loading:t.loading,columns:t.columns,data:t.data}}),t._v(" "),t.pagination.count>0?n("Page",{attrs:{current:t.pagination.page,total:t.pagination.count,"class-name":"gap-top","show-elevator":""},on:{"on-change":t.pageChange}}):t._e()],1)},staticRenderFns:[]},u=n("VU/8")(d,l,!1,null,null,null).exports,_=n("woOf"),p=n.n(_),m=n("pFYg"),h=n.n(m),v=n("d7EF"),f=n.n(v),y=n("+6Bu"),g=n.n(y),w=n("mvHQ"),T=n.n(w),I=n("fZjL"),E=n.n(I),b=n("BO1k"),k=n.n(b),S=function(t,e){var n=e.type,i=g()(e,["type"]),a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r={},s=document.querySelector("input[name=csrfmiddlewaretoken]");return a=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=new URLSearchParams,i=!0,a=!1,r=void 0;try{for(var s,o=k()(E()(t));!(i=(s=o.next()).done);i=!0){var c=s.value;n.append(c,t[c]instanceof Object?T()(t[c]):t[c])}}catch(t){a=!0,r=t}finally{try{!i&&o.return&&o.return()}finally{if(a)throw r}}return e.Accept="application/json",e["Content-Type"]="application/x-www-form-urlencoded; charset=utf-8",{method:"POST",body:n,headers:e}}({type:n,data:i},a),s&&(r["X-CSRFToken"]=s.value),a.headers&&(r=p()({},r,a.headers||{})),fetch(t,p()({method:"POST",cache:"no-cache",credentials:"include"},a,{headers:r}))},C=function(t,e){return{status:!0,code:0,msg:{count:e||t.length,page_count:1,page:1,has_prev:!1,has_next:!1,datas:F(t)}}},L=function(t){return{status:!0,code:0,msg:F(t)}},R=function(t,e,n){if(-1===n.code)return n;var i=t.split("."),a=i.slice(-1),r=f()(a,1)[0],s=i.slice(0,-1).reduce(function(t,e){return t?t[e]:null},n);return s&&(s[r]=s[r].map(e)),n},F=function t(e){return"object"===(void 0===e?"undefined":h()(e))?e.length?e.map(t):c()({},e):e},$=function(t){return t?t.getFullYear()+"-"+(t.getMonth()+1)+"-"+t.getDate():t},N=function(t){return{id:t.id,company_id:parseInt(t.companyId),amount:t.amount,borrower_id:t.borrower_id,entity_id:t.entity_id,signer_id:t.signer_id,sign_date:$(t.sign_date||void 0),borrow_date:$(t.borrow_date||void 0),revert_borrow_date:$(t.revert_borrow_date||void 0),revert_date:$(t.revert_date||void 0),descript:t.descript,status:t.status}},O=[],P={name:"ListEntity",props:["companyId"],data:function(){var t=this;return{loading:!1,editEntitys:{},editEntitysTop:0,columns:[{type:"selection",align:"center",width:60},{type:"index",align:"center",width:60},{title:"物品",key:"entity"},{title:"数量",key:"amount",width:60},{title:"签收人",key:"signer"},{title:"签收日期",key:"sign_date"},{title:"借用人",key:"borrower"},{title:"借用日期",key:"borrow_date"},{title:"归还日期",key:"revert_borrow_date"},{title:"状态",key:"status",width:60},{title:"备注",key:"descript"},{title:"操作",key:"action",align:"center",render:function(e,n){return e("div",[e("Button",{props:{type:"primary",size:"small",disabled:n.row._disabled},on:{click:function(e){t.updateEntity(n.row,e)}}},"修改")])}}]}},computed:{pagination:function(){return this.$store.state.pagination.data},data:function(){return this.$store.getters.entitys},result:function(){return this.data.length?this.data:[]}},methods:{addEntity:function(){this.$router.push({name:"BatchAddEntitys",params:{companyId:this.companyId}})},updateEntity:function(t,e){this.editEntitysTop=this.getOffsetByTable(e),i.default.set(this,"editEntitys",p()({removed:!1},t))},cancelEdit:function(){i.default.set(this,"editEntitys",{})},commitEdit:function(){var t=N(p()({companyId:this.companyId},this.editEntitys));return this.$store.dispatch("UPDATE_ENTITYS",{datas:[t]}).then(this.getRevertedEntitys).then(this.cancelEdit)},getOffsetByTable:function(t){var e=t.path[8].getBoundingClientRect();return t.clientY-e.top},selectChange:function(t){O=t},getRevertedEntitys:function(){var t=this;return this.loading=!0,this.$store.dispatch("FILTER_ENTITYS_ALL_LIST",{company_id:parseInt(this.companyId),status:"归还"}).then(function(){t.loading=!1})},revertEntity:function(){var t=this;0!==O.length?this.$store.dispatch("REVERT_ENTITYS",{selected:O.map(function(t){return t.id}),company_id:parseInt(this.companyId)}).then(function(e){var n=e.msg,i=O.map(function(t){return{entity:t.entity,amount:t.amount}});O=[],t.$router.push({name:"Print",params:{companyId:t.companyId,entitys:i,orderId:n}})}):this.$store.dispatch("SHOW_NOTIFY",{title:"还没选择归还物品",type:"warning"})}},created:function(){var t=this;this.getRevertedEntitys(),this.$store.dispatch("FETCH_COMPANY_LIST",{id:parseInt(this.companyId)}).then(function(){var e=t.$store.getters.companyById(parseInt(t.companyId));t.$store.commit("SET_BREADCRUMB",{name:t.$options.name,title:e.title})})}},x={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"list-entitys-container"},[n("Table",{attrs:{loading:t.loading,columns:t.columns,data:t.result},on:{"on-selection-change":t.selectChange}}),t._v(" "),Object.keys(t.editEntitys).length?n("Form",{staticClass:"edit-entitys-wrap"},[n("div",{staticClass:"edit-entitys-position",style:{top:t.editEntitysTop+"px"}},[n("entitys",{attrs:{item:t.editEntitys,successBtnText:"确认",cancelBtnText:"取消"},on:{handleCancel:function(e){t.cancelEdit()},handleSuccess:function(e){t.commitEdit()}}})],1)]):t._e(),t._v(" "),n("div",{staticClass:"gap-top"},[n("Button",{attrs:{type:"warning"},on:{click:t.addEntity}},[t._v("资料录入")]),t._v(" "),n("Button",{attrs:{type:"info"},on:{click:t.revertEntity}},[t._v("归还")]),t._v(" "),n("Button",{attrs:{type:"default"},on:{click:function(e){t.$router.back()}}},[t._v("后退")])],1),t._v(" "),n("router-view")],1)},staticRenderFns:[]};var A=n("VU/8")(P,x,!1,function(t){n("JPGY")},null,null).exports,Y=n("//Fk"),B=n.n(Y),D={props:["companyId"],data:function(){return{defaultFormItem:{entity_id:"",amount:0,signer_id:"",sign_date:void 0,borrower_id:void 0,borrow_date:void 0,revert_borrow_date:void 0,revert_date:void 0,status:"寄存",descript:"",removed:!1},formItems:{items:[]},spinShow:!1}},methods:{addEntitys:function(){var t=this,e=this.formItems.items.filter(function(t){return!t.removed&&t.entity_id}).map(function(e){return N(p()({companyId:t.companyId},e))});return e.length?this.$store.dispatch("UPDATE_ENTITYS",{datas:e}):B.a.reject(new Error("请至少添加一条资料"))},handleSubmit:function(t){var e=this;this.spinShow=!0,this.addEntitys().then(function(){e.spinShow=!1,e.$store.dispatch("SHOW_NOTIFY",{title:"提交成功",type:"info"}),e.$router.back()}).catch(function(t){e.spinShow=!1,e.$store.dispatch("SHOW_NOTIFY",{title:"提交错误",desc:t,type:"error"})})},handleReset:function(t){this.$refs[t].resetFields()},handleAdd:function(){this.formItems.items.push(p()({},this.defaultFormItem))},handleRemove:function(t){this.formItems.items[t].removed=!0}},created:function(){this.handleAdd()}},V={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Form",{ref:"formItems",attrs:{model:t.formItems}},[t._l(t.formItems.items,function(e,i){return e.removed?t._e():n("FormItem",{key:i},[n("entitys",{attrs:{item:e,cancelBtnText:"删除"},on:{handleCancel:function(e){t.handleRemove(i)}}})],1)}),t._v(" "),n("FormItem",[n("Button",{staticStyle:{width:"100px"},attrs:{type:"dashed",long:"",icon:"plus-round"},on:{click:t.handleAdd}},[t._v("添加")])],1),t._v(" "),n("FormItem",[n("Button",{attrs:{type:"primary"},on:{click:function(e){t.handleSubmit("formItems")}}},[t._v("提交")]),t._v(" "),n("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:function(e){t.$router.back()}}},[t._v("取消")])],1)],2),t._v(" "),t.spinShow?n("Spin",{attrs:{size:"large",fix:""}}):t._e()],1)},staticRenderFns:[]},H=n("VU/8")(D,V,!1,null,null,null).exports,M=n("c/Tr"),U=n.n(M),G={name:"Print",props:["entitys","companyId","orderId","orderDateTime"],data:function(){return{columns:[{type:"index",align:"center",width:60},{title:"物品",key:"entity"},{title:"数量",key:"amount",width:60}]}},computed:{client:function(){return this.$store.getters.companyById(parseInt(this.companyId))||{}},now:function(){return this.orderDateTime||new Date}},methods:{startPrint:function(){window.print()}},created:function(){var t=this,e=Math.max(this.entitys.length+(this.entitys.length%2?5:4),10),n=U()({length:e},function(e,n){return t.entitys[n]||{entity:"",amount:""}});this.entitysLeft=n.slice(0,e/2),this.entitysRight=n.slice(e/2),this.$store.dispatch("FETCH_COMPANY_LIST",{id:this.companyId})}},z={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"wrapp-print"},[n("div",{staticClass:"print"},[n("div",{staticClass:"header nav"},[n("div",{staticClass:"nav-item width20"}),t._v(" "),n("div",{staticClass:"nav-item width55"},[n("img",{staticClass:"logo",attrs:{src:t.$store.state.config.logoImg}}),t._v(" "),n("h2",{staticClass:"height-half"},[t._v(" "+t._s(t.$store.state.config.companyName)+" ")]),t._v(" "),n("h2",{staticClass:"height-half"},[t._v(" 客户证件（资料）交接表 ")])]),t._v(" "),n("div",{staticClass:"nav-item width25"},[n("div",{staticClass:"height-half doub-h2-lh"},[t._v(" 编号："+t._s(t.orderId)+" ")]),t._v(" "),n("div",{staticClass:"height-half doub-h2-lh"},[t._v(" "+t._s(t.now.getFullYear())+" 年 "+t._s(t.now.getMonth()+1)+" 月 "+t._s(t.now.getDate())+" 日 ")])])]),t._v(" "),n("h2",[t._v("今收到（交还）"),n("u",[t._v(t._s(t.client.title))]),t._v(" 证件（资料）如下：")]),t._v(" "),n("div",{staticClass:"table"},[n("div",{staticClass:"width50"},[n("table",{attrs:{border:"1",cellspacing:"0"}},[t._m(0),t._v(" "),n("tbody",t._l(t.entitysLeft,function(e,i){return n("tr",{key:i},[n("td",[t._v(t._s(i+1))]),t._v(" "),n("td",[t._v(t._s(e.entity))]),t._v(" "),n("td",[t._v(t._s(e.amount))])])}))])]),t._v(" "),n("div",{staticClass:"width50"},[n("table",{staticStyle:{"border-left":"0"},attrs:{border:"1",cellspacing:"0"}},[t._m(1),t._v(" "),n("tbody",t._l(t.entitysRight,function(e,i){return n("tr",{key:i},[n("td",[t._v(t._s(i+1+t.entitysLeft.length))]),t._v(" "),n("td",[t._v(t._s(e.entity))]),t._v(" "),n("td",[t._v(t._s(e.amount))])])}))])])]),t._v(" "),n("div",{staticClass:"gap-top"},[t._m(2),t._v(" "),n("div",{staticClass:"nav"},[n("span",{staticClass:"nav-item width50"},[t._v("负责人："+t._s(t.client.contactor))]),t._v(" "),n("span",{staticClass:"nav-item width50"},[t._v("网址：www.gzyhcs.com")])]),t._v(" "),n("div",{staticClass:"nav"},[n("span",{staticClass:"nav-item width50"},[t._v("负责人电话："+t._s(t.client.contactor_phone))]),t._v(" "),n("span",{staticClass:"nav-item width50"},[t._v("咨询电话：020-87313109")])]),t._v(" "),n("div",{staticClass:"nav"},[n("span",{staticClass:"nav-item width50"},[t._v("客户地址："+t._s(t.client.op_address))]),t._v(" "),n("span",{staticClass:"nav-item width50"},[t._v("地址：广州越秀区永福路8号永怡新都808室")])])]),t._v(" "),n("Button",{attrs:{type:"info"},on:{click:t.startPrint}},[t._v("开始打印")])],1)])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",[this._v("序号")]),this._v(" "),e("th",[this._v("物品")]),this._v(" "),e("th",[this._v("数量")])])])},function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",[this._v("序号")]),this._v(" "),e("th",[this._v("物品")]),this._v(" "),e("th",[this._v("数量")])])])},function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"nav"},[e("span",{staticClass:"nav-item width50"},[this._v("以上证件（资料）共计："),e("u",[this._v("        ")]),this._v(" 项")]),this._v(" "),e("span",{staticClass:"nav-item width25"},[this._v("接收人：")]),this._v(" "),e("span",{staticClass:"nav-item width25"},[this._v("移交人：")])])}]};var j=n("VU/8")(G,z,!1,function(t){n("30Op")},"data-v-ce1bab00",null).exports,W=n("NYxO"),Q={name:"ListRevertEntity",data:function(){var t=this;return{loading:!1,columns:[{type:"index",align:"center",width:60},{title:"公司",key:"company"},{title:"归还编号",key:"order_id",width:150},{title:"归还日期",key:"revert_borrow_date",width:120},{title:"操作",key:"action",align:"center",width:80,render:function(e,n){return e("div",[e("Button",{props:{type:"primary",size:"small"},on:{click:function(){t.handleShowDetails(n.row)}}},"详情")])}}],search:{order_id:void 0,company:""}}},computed:c()({pagination:function(){return this.$store.state.pagination.data}},Object(W.b)(["revertList","entitys"])),methods:{handleSearch:function(){var t=this,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1,n=p()({},this.search,{page:e});this.loading=!0,this.$store.dispatch("FILTER_REVERTLIST",n).then(function(n){t.$store.commit("SET_PAGINATION_PAGE",e),t.$store.commit("SET_PAGINATION_COUNT",n.msg.count),t.loading=!1})},handleShowDetails:function(t){var e=this;this.$store.dispatch("GET_ENTITYS_REVERT",{order_id:t.order_id,id:t.id}).then(function(){e.$router.push({name:"Print2",params:{entitys:e.entitys,companyId:t.company_id,orderId:t.order_id,orderDateTime:new Date(t.revert_borrow_date)}})})}},created:function(){this.handleSearch()}},J={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Card",[n("Form",{attrs:{model:t.search}},[n("Row",[n("Col",{attrs:{span:"8"}},[n("Input",{model:{value:t.search.order_id,callback:function(e){t.$set(t.search,"order_id",e)},expression:"search.order_id"}},[n("span",{attrs:{slot:"prepend"},slot:"prepend"},[t._v(" 归还编号：")])])],1),t._v(" "),n("Col",{attrs:{span:"8"}},[n("Input",{model:{value:t.search.company,callback:function(e){t.$set(t.search,"company",e)},expression:"search.company"}},[n("span",{attrs:{slot:"prepend"},slot:"prepend"},[t._v(" 公司：")])])],1),t._v(" "),n("Col",{attrs:{span:"8"}},[n("Button",{attrs:{type:"info"},on:{click:function(e){t.handleSearch()}}},[t._v("搜索")]),t._v(" "),n("Button",{attrs:{type:"default"},on:{click:function(e){t.$router.back()}}},[t._v("后退")])],1)],1)],1)],1),t._v(" "),n("div",{staticClass:"gap-top"}),t._v(" "),n("Table",{attrs:{loading:t.loading,columns:t.columns,data:t.revertList}}),t._v(" "),t.pagination.count>0?n("Page",{attrs:{current:t.pagination.page,total:t.pagination.count,"class-name":"gap-top","show-elevator":""},on:{"on-change":t.handleSearch}}):t._e()],1)},staticRenderFns:[]},X=n("VU/8")(Q,J,!1,null,null,null).exports,Z={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("Content",{staticClass:"content"},[n("Breadcrumb",{staticClass:"breadcrumb"},t._l(t.$route.matched,function(e,i){return e.meta.bcSkip?t._e():n("BreadcrumbItem",{key:i},[t._v("\n        "+t._s(t.$store.state.breadcrumb.data[e.meta.bcName||e.name]||e.meta.title)+"\n        ")])})),t._v(" "),n("Card",[n("router-view")],1)],1)},staticRenderFns:[]};var q,K=n("VU/8")({},Z,!1,function(t){n("7dH6")},"data-v-3c4a4ef2",null).exports,tt={render:function(){var t=this.$createElement;return(this._self._c||t)("router-view")},staticRenderFns:[]},et=n("VU/8")({},tt,!1,null,null,null).exports,nt={props:["item","cancelBtnText","successBtnText"],data:function(){return{dateOptions:{shortcuts:[{text:"今天",value:function(){return new Date}}]},searchPeopleLoading:!1,defaultFormSigner:this.item.signer||"",defaultFormBorrower:this.item.borrower||""}},methods:{handlePeopleSearch:(q=void 0,function(t){var e=this;""!==t&&(q&&clearTimeout(q),q=setTimeout(function(){q=void 0,e.searchPeopleLoading=!0,e.$store.dispatch("FILTER_PEOPLES_LIST",{name:t}).then(function(){e.searchPeopleLoading=!1})},200))}),handleCancel:function(){this.$emit("handleCancel")},handleSuccess:function(){this.$emit("handleSuccess")}},computed:Object(W.b)(["entityList","peoples"]),created:function(){this.$store.dispatch("FILTER_ENTITY_LIST")}},it={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"fields"},[n("div",{staticClass:"field"},[n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"物品："}},[n("Select",{staticStyle:{width:"10rem"},attrs:{filterable:""},model:{value:t.item.entity_id,callback:function(e){t.$set(t.item,"entity_id",e)},expression:"item.entity_id"}},t._l(t.entityList,function(e){return n("Option",{key:e.id,attrs:{value:e.id}},[t._v(t._s(e.name))])}))],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"数量："}},[n("InputNumber",{staticStyle:{width:"5rem"},attrs:{min:0},model:{value:t.item.amount,callback:function(e){t.$set(t.item,"amount",e)},expression:"item.amount"}})],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"签收人："}},[n("Select",{staticStyle:{width:"10rem"},attrs:{filterable:"",remote:"",label:t.defaultFormSigner,"remote-method":t.handlePeopleSearch,loading:t.searchPeopleLoading},model:{value:t.item.signer_id,callback:function(e){t.$set(t.item,"signer_id",e)},expression:"item.signer_id"}},t._l(t.peoples,function(e){return n("Option",{key:e.id,attrs:{value:e.id}},[t._v(t._s(e.name))])}))],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"签收日期："}},[n("DatePicker",{staticStyle:{width:"10rem"},attrs:{type:"date",options:t.dateOptions},model:{value:t.item.sign_date,callback:function(e){t.$set(t.item,"sign_date",e)},expression:"item.sign_date"}})],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"借用人："}},[n("Select",{staticStyle:{width:"10rem"},attrs:{filterable:"",remote:"",label:t.defaultFormBorrower,"remote-method":t.handlePeopleSearch,loading:t.searchPeopleLoading},model:{value:t.item.borrower_id,callback:function(e){t.$set(t.item,"borrower_id",e)},expression:"item.borrower_id"}},t._l(t.peoples,function(e){return n("Option",{key:e.id,attrs:{value:e.id}},[t._v(t._s(e.name))])}))],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"借用日期："}},[n("DatePicker",{staticStyle:{width:"10rem"},attrs:{type:"date",options:t.dateOptions},model:{value:t.item.borrow_date,callback:function(e){t.$set(t.item,"borrow_date",e)},expression:"item.borrow_date"}})],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"还回日期："}},[n("DatePicker",{staticStyle:{width:"10rem"},attrs:{type:"date",options:t.dateOptions},model:{value:t.item.revert_borrow_date,callback:function(e){t.$set(t.item,"revert_borrow_date",e)},expression:"item.revert_borrow_date"}})],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"归还日期："}},[n("DatePicker",{staticStyle:{width:"10rem"},attrs:{type:"date",options:t.dateOptions},model:{value:t.item.revert_date,callback:function(e){t.$set(t.item,"revert_date",e)},expression:"item.revert_date"}})],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"状态："}},[n("Select",{model:{value:t.item.status,callback:function(e){t.$set(t.item,"status",e)},expression:"item.status"}},[n("Option",{attrs:{value:"寄存"}},[t._v("寄存")]),t._v(" "),n("Option",{attrs:{value:"借出"}},[t._v("借出")]),t._v(" "),n("Option",{attrs:{value:"归还"}},[t._v("归还")])],1)],1)],1),t._v(" "),n("div",{staticClass:"item"},[n("FormItem",{attrs:{label:"备注："}},[n("Input",{attrs:{type:"textarea",autosize:{minRows:2,maxRows:5}},model:{value:t.item.descript,callback:function(e){t.$set(t.item,"descript",e)},expression:"item.descript"}})],1)],1)]),t._v(" "),n("div",{staticClass:"field-opt"},[n("Button",{attrs:{type:"ghost"},on:{click:t.handleCancel}},[t._v(t._s(t.cancelBtnText))]),t._v(" "),t.successBtnText?n("Button",{attrs:{type:"ghost"},on:{click:t.handleSuccess}},[t._v(t._s(t.successBtnText))]):t._e()],1)])},staticRenderFns:[]};var at=n("VU/8")(nt,it,!1,function(t){n("h6nX")},"data-v-1fc4b690",null).exports;i.default.use(s.a),i.default.component("entitys",at);var rt=new s.a({routes:[{path:"/company/:companyId?",name:"Main",component:K,meta:{title:"资料借用"},children:[{path:"",name:"ListCompany",component:u,meta:{title:"公司列表"}},{path:"entity",name:"EntityContainer",component:et,meta:{bcName:"ListEntity",title:"资料列表"},children:[{path:"",name:"ListEntity",component:A,props:!0,meta:{bcSkip:!0,title:""}},{path:"add",name:"BatchAddEntitys",component:H,props:!0,meta:{title:"资料录入"}},{path:"revert/print",name:"Print",component:j,props:!0,meta:{title:"资料归还"}}]}]},{path:"/revertentitys",name:"Main",component:K,meta:{title:"已归还资料列表"},children:[{path:"",name:"ListRevertEntity",component:X,meta:{title:"归还单"}},{path:"revert/print",name:"Print2",component:j,props:!0,meta:{title:"资料归还"}}]},{path:"",redirect:"/company"}]}),st=n("Zrlr"),ot=n.n(st),ct=n("wxAW"),dt=n.n(ct),lt=function(t){return t.json()},ut=function(){function t(e){ot()(this,t),this._url=e}return dt()(t,[{key:"fakeApiData",value:function(){return{status:!0,msg:"",code:0}}},{key:"_fakeApiData",value:function(){for(var t=arguments.length,e=Array(t),n=0;n<t;n++)e[n]=arguments[n];return console.log("fetch api: ",this.constructor.name,e),this.fakeApiData.apply(this,e)}},{key:"fetch",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return this._devMode?B.a.resolve(this._fakeApiData(t,e)):S(this._url,t,e).then(lt)}}]),t}();ut.prototype._devMode=!1;var _t,pt,mt,ht=ut,vt=n("bOdI"),ft=n.n(vt),yt=n("Zx67"),gt=n.n(yt),wt=n("zwoO"),Tt=n.n(wt),It=n("Pf15"),Et=n.n(It),bt=[{id:1,title:"部落胜利有限公司",address:"地球某地",saleman:"小皮球",bookkeeper:"",industry:"",taxpayer_type:"",license_status:"有效",status:"有效",contactor:"洛瑟玛·塞隆",contactor_phone:"12345678901"},{id:2,title:"亡灵大叫有限公司",address:"地球某地",saleman:"不穿衣",bookkeeper:"",industry:"",taxpayer_type:"",license_status:"有效",status:"有效",contactor:"希尔瓦娜斯·风行者",contactor_phone:"12345678901"},{id:3,title:"联盟太衰有限公司",address:"地球某地",saleman:"性感猫咪",bookkeeper:"",industry:"",taxpayer_type:"",license_status:"有效",status:"有效",contactor:"瓦里安·乌瑞恩国王",contactor_phone:"12345678901"}],kt=new(function(t){function e(){return ot()(this,e),Tt()(this,(e.__proto__||gt()(e)).apply(this,arguments))}return Et()(e,t),dt()(e,[{key:"fakeApiData",value:function(t){switch(t.type){case"api_filter":var e=bt;t.title&&(e=e.filter(function(e){return e.title.includes(t.title)})),t.id&&(e=e.filter(function(e){return e.id===t.id}));var n=e.length,i=2*((t.page||1)-1),a=e.slice(i,i+2);return C(a,n);default:return{status:!1,code:-100,msg:""}}}},{key:"genCustomField",value:function(t){return p()({contactor_info:t.contactor+" "+t.contactor_phone},t)}},{key:"filter",value:function(t){return this.fetch(c()({type:"api_filter"},t)).then(R.bind(null,"msg.datas",this.genCustomField))}}]),e}(ht))("/borrow/api/company"),St="YH201804010010",Ct=[{id:1,entity:"证明",amount:1,signer:"admin",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"寄存",descript:"test",entity_id:3,signer_id:1,borrower_id:2,company_id:1},{id:4,entity:"身份证",amount:1,signer:"admin",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"寄存",descript:"test",entity_id:3,signer_id:1,borrower_id:2,company_id:1},{id:5,entity:"证明",amount:1,signer:"admin",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"寄存",descript:"test",entity_id:3,signer_id:1,borrower_id:2,company_id:1},{id:6,entity:"证明",amount:1,signer:"admin",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"寄存",descript:"test",entity_id:3,signer_id:1,borrower_id:2,company_id:1},{id:7,entity:"身份证",amount:1,signer:"admin",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"寄存",descript:"test",entity_id:3,signer_id:1,borrower_id:2,company_id:1,order_id:St},{id:2,entity:"护照",amount:2,signer:"雇员2",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"归还",descript:"test",entity_id:2,signer_id:3,borrower_id:2,company_id:1,order_id:St},{id:3,entity:"证明",amount:2,signer:"雇员2",sign_date:"2018-03-08",borrower:"雇员1",borrow_date:"2018-03-11",revert_borrow_date:"2018-04-11",revert_date:"2018-04-23",status:"归还",descript:"test",entity_id:2,signer_id:3,borrower_id:2,company_id:2,order_id:St}],Lt=new(function(t){function e(){return ot()(this,e),Tt()(this,(e.__proto__||gt()(e)).apply(this,arguments))}return Et()(e,t),dt()(e,[{key:"fakeApiData",value:function(t){switch(t.type){case"api_get_revert":return L(Ct.filter(function(e){return e.order_id===t.order_id}));case"api_filter":return C(Ct.filter(function(e){return e.company_id===t.company_id&&e.status===t.status}));case"api_filter_all":return L(Ct.filter(function(e){return e.company_id===t.company_id&&e.status!==t.status}));case"api_update":return Ct=Array.prototype.concat.call([],Ct,t.datas),L(!0);case"api_revert":var e=Ct.filter(function(e){return t.selected.includes(e.id)});return e?(e.forEach(function(t){t.status="归还",t.order_id=St}),L(St)):this.fakeApiData({type:"default"});default:return{status:!1,code:-100,msg:""}}}},{key:"filter",value:function(t){return this.fetch(c()({type:"api_filter"},t))}},{key:"filterAll",value:function(t){return this.fetch(c()({type:"api_filter_all"},t))}},{key:"update",value:function(t){return this.fetch(c()({type:"api_update"},t))}},{key:"revert",value:function(t){return this.fetch(c()({type:"api_revert"},t))}},{key:"getRevert",value:function(t){return this.fetch(c()({type:"api_get_revert"},t))}}]),e}(ht))("/borrow/api/entity_list"),Rt=new(function(t){function e(){return ot()(this,e),Tt()(this,(e.__proto__||gt()(e)).apply(this,arguments))}return Et()(e,t),dt()(e,[{key:"fakeApiData",value:function(t){switch(t.type){case"api_filter":return L([{id:1,name:"身份证"},{id:2,name:"护照"},{id:3,name:"证明"}]);default:return{status:!1,code:-100,msg:""}}}},{key:"filter",value:function(){return this.fetch({type:"api_filter"})}}]),e}(ht))("/borrow/api/entity"),Ft=[{id:1,first_name:"雇员1",last_name:""},{id:2,first_name:"雇员2",last_name:""},{id:3,first_name:"张三",last_name:""},{id:4,first_name:"fake user",last_name:""}],$t=new(function(t){function e(){return ot()(this,e),Tt()(this,(e.__proto__||gt()(e)).apply(this,arguments))}return Et()(e,t),dt()(e,[{key:"fakeApiData",value:function(t){switch(t.type){case"api_filter":return L(Ft.filter(function(e){return e.first_name.includes(t.name)}));default:return{status:!1,code:-100,msg:""}}}},{key:"genCustomField",value:function(t){return p()({name:""+t.last_name+t.first_name},t)}},{key:"filter",value:function(t){return this.fetch(c()({type:"api_filter"},t)).then(R.bind(null,"msg",this.genCustomField))}}]),e}(ht))("/borrow/api/people"),Nt=[{id:1,company:"部落胜利有限公司",company_id:1,order_id:"YH201804010010",revert_borrow_date:"2018-04-12"},{id:2,company:"部落胜利有限公司",company_id:1,order_id:"YH201804010011",revert_borrow_date:"2018-04-13"},{id:3,company:"亡灵大叫有限公司",company_id:2,order_id:"YH201804010012",revert_borrow_date:"2018-04-14"}],Ot=new(function(t){function e(){return ot()(this,e),Tt()(this,(e.__proto__||gt()(e)).apply(this,arguments))}return Et()(e,t),dt()(e,[{key:"fakeApiData",value:function(t){switch(t.type){case"api_filter":return C(Nt);default:return{status:!1,code:-100,msg:""}}}},{key:"filter",value:function(t){return this.fetch(c()({type:"api_filter"},t))}}]),e}(ht))("/borrow/api/revert_list"),Pt=n("BTaQ"),xt=n.n(Pt),At={info:Pt.Notice.info,success:Pt.Notice.success,warning:Pt.Notice.warning,error:Pt.Notice.error,default:Pt.Notice.open},Yt={state:{},actions:ft()({},"SHOW_NOTIFY",function(t,e){return function(t){var e=t.type,n=void 0===e?"default":e,i=t.title,a=t.desc,r=void 0===a?"":a,s=t.duration,o=void 0===s?4.5:s;return new B.a(function(t){At[n].call(Pt.Notice,{title:i,desc:r,duration:o,onClose:t})})}.call(this,e)})},Bt={state:{data:{count:100,page:1,size:10}},mutations:(_t={},ft()(_t,"SET_PAGINATION_COUNT",function(t,e){i.default.set(t.data,"count",e)}),ft()(_t,"SET_PAGINATION_PAGE",function(t,e){i.default.set(t.data,"page",e)}),_t)},Dt={state:{data:{}},mutations:ft()({},"SET_BREADCRUMB",function(t,e){var n=e.name,a=e.title;i.default.set(t.data,n,a)})};i.default.use(W.a);var Vt=function(t){return new B.a(function(e,n){t.then(function(t){t.status?e(t):(jt.dispatch("SHOW_NOTIFY",{title:t.msg||"未知错误",type:"error",duration:0}),n(t))}).catch(function(t){console.error(t),jt.dispatch("SHOW_NOTIFY",{title:"网络出错！",type:"error",duration:0})})})},Ht={state:{companyList:[]},getters:{companyList:function(t){return t.companyList},companyById:function(t){return function(e){return t.companyList.find(function(t){return t.id===e})}}},mutations:ft()({},"FETCH_COMPANY_LIST",function(t,e){i.default.set(t,"companyList",e)}),actions:ft()({},"FETCH_COMPANY_LIST",function(t,e){var n=t.commit;t.state;return Vt(kt.filter(e)).then(function(t){return n("FETCH_COMPANY_LIST",t.msg.datas),t})})},Mt={state:{revertList:[],revertEnttiyList:[]},getters:{revertList:function(t){return t.revertList}},mutations:ft()({},"FILTER_REVERTLIST",function(t,e){i.default.set(t,"revertList",e)}),actions:ft()({},"FILTER_REVERTLIST",function(t,e){var n=t.commit;return Vt(Ot.filter(e)).then(function(t){return n("FILTER_REVERTLIST",t.msg.datas),t})})},Ut={state:{entityList:[]},getters:{entityList:function(t){return t.entityList}},mutations:ft()({},"FILTER_ENTITY_LIST",function(t,e){i.default.set(t,"entityList",e)}),actions:ft()({},"FILTER_ENTITY_LIST",function(t){var e=t.commit,n=t.state;return n.entityList.length>0?B.a.resolve(n.entityList):Rt.filter().then(function(t){return e("FILTER_ENTITY_LIST",t.msg),t})})},Gt={state:{entitys:[]},getters:{entitys:function(t){return t.entitys}},mutations:(pt={},ft()(pt,"FILTER_ENTITYS_LIST",function(t,e){i.default.set(t,"entitys",e)}),ft()(pt,"REVERT_ENTITYS",function(t,e){var n=t.entitys.filter(function(t){return e.selected.includes(t.id)});n.length>0&&n.forEach(function(t){i.default.set(t,"status","归还")})}),ft()(pt,"GET_ENTITYS_REVERT",function(t,e){i.default.set(t,"entitys",e)}),pt),actions:(mt={},ft()(mt,"FILTER_ENTITYS_LIST",function(t,e){var n=t.commit;return Vt(Lt.filter(e)).then(function(t){return n("FILTER_ENTITYS_LIST",t.msg.datas),t})}),ft()(mt,"FILTER_ENTITYS_ALL_LIST",function(t,e){var n=t.commit;return Vt(Lt.filterAll(e)).then(function(t){return n("FILTER_ENTITYS_LIST",t.msg),t})}),ft()(mt,"UPDATE_ENTITYS",function(t,e){t.commit;return Vt(Lt.update(e))}),ft()(mt,"REVERT_ENTITYS",function(t,e){var n=t.commit;return Vt(Lt.revert(e)).then(function(t){return n("REVERT_ENTITYS",e),t})}),ft()(mt,"GET_ENTITYS_REVERT",function(t,e){var n=t.commit;return Vt(Lt.getRevert(e)).then(function(t){return n("GET_ENTITYS_REVERT",t.msg),t})}),mt)},zt={state:{peoples:[]},getters:{peoples:function(t){return t.peoples}},mutations:ft()({},"FILTER_PEOPLES_LIST",function(t,e){i.default.set(t,"peoples",e)}),actions:ft()({},"FILTER_PEOPLES_LIST",function(t,e){var n=t.commit;return $t.filter(e).then(function(t){return n("FILTER_PEOPLES_LIST",t.msg),t})})},jt=new W.a.Store({modules:{config:{state:{companyName:"广州悦海财税代理有限公司",logoImg:"/static/img/logo.png",adminUrl:"/admin/"}},company:Ht,entity:Ut,entitys:Gt,people:zt,revertList:Mt,breadcrumb:Dt,notify:Yt,pagination:Bt},strict:!0}),Wt=jt;n("+skl");ht.prototype._devMode=window._devMode||!1,i.default.config.productionTip=!1,i.default.use(xt.a),new i.default({el:"#app",store:Wt,router:rt,components:{App:r},template:"<App />"})},gz2f:function(t,e){},h6nX:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.8db27a1c8fa24e9f920a.js.map