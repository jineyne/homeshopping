var datas = {
    current_time: new Date(2017, 11, 25, 13, 00),
    top: {
        date: new Date(2017, 11, 25, 13, 00),
        done: false
    },
    bottom: {
        date: new Date(2017, 11, 25, 13, 00),
        done: false
    }
}

var is_loading = false;

var filter_mall = "";
var filter_ct = "";

function percentage(small, big) {
    return Math.floor((small / big) * 100);
}

function load_lazy() {
    $('img[src=""]').each((i, e) => {
        $(e).lazyload({ threshold: 200 })
    });
}

function make_filter() {
    filter = filter_mall;
    if (filter === "") {
        filter = filter_ct;
    } else if (filter !== "" && filter_ct !== "") {
        filter += ":" + filter_ct;
    } else if (filter !== "" && filter_ct === "") {
    }

    return filter;
}

function clear() {
    var temp = []
    $("div[id^='date-stemp-']").each((i, e) => {
        if (temp.indexOf(e.id) === -1) {
            temp.push(e.id);
        } else {
            e.remove();
        }
    });
}

function load_header() {
    $.ajax({
        url: "http://localhost:5000/cate",
        method: "GET",
        cache: true,
        dataType: "json",
        success: (data, s, xhr) => {
            if (xhr.status === 200) {
                data.forEach((v, i, d) => {
                    if (v.name !== undefined && v.name !== "") {
                        $("#select-category")
                            .append(`<option value="ct|${v.name}">
                                        ${v.name}
                                     </option>`);
                    }
                });
            }
        },
        error: (err) => {
            
        }
    });

    $.ajax({
        url: "http://localhost:5000/mall",
        method: "GET",
        cache: true,
        dataType: "json",
        success: (data, s, xhr) => {
            if (xhr.status === 200) {
                data.forEach((v, i, d) => {
                    if (v.name !== undefined && v.name !== "") {
                        $("#select-mall")
                            .append(`<option value="m|${v.name}">
                                        ${v.label}
                                     </option>`);
                    }
                });
            }
        },
        error: (err) => {

        }
    });
}

function build(items, cb, cb_on_error=null) {
    $.ajax({
        url: "./build",
        method: "POST",
        dataType: "html",
        data: {
            items,
            csrfmiddlewaretoken: csrf_token
        },
        success: (data) => {
            cb(data)
            clear();
            load_lazy();
        },
        error: (err) => {
            if (err.status === 404 && err.responseText !== undefined) {
                if (cb_on_error !== null) {
                    cb_on_error()
                }
            }
        },
        complete: () => {
            is_loading = false;
        }
    });
}

function load_data(args, cb, cb_on_error=null, cb_done=null) {
    var url = "http://localhost:5000/item/ft/date/time/asc";
    url = url.replace("ft", args.ft || "all");
    url = url.replace("date", args.date ||
        datas.current_time.format("yyyyMMdd"));
    url = url.replace("time", args.time ||
        datas.current_time.format("HHmm"));
    url = url.replace("asc", args.asc || "asc");

    is_loading = true;

    $.ajax({
        url: url,
        method: "GET",
        dataType: "text",
        success: (data, s, xhr) => {
            if (xhr.status === 204) {
                is_loading = false;
                if (cb_on_error !== null) {
                    cb_on_error()
                }
            } else {
                build(data, cb, cb_on_error);
            }
        },
        error: (err) => {
            is_loading = false;
            if (err.status === 409) {
                cb("<div style='width:100%; height:100px; \
                        background-color=red;'> \
                        <div class='center'> \
                            더이상 제품이 존재하지 않습니다. \
                        </div> \
                    </div>");
                if (cb_done !== null) {
                    cb_done();
                }
            }
        }
    });
}

function on_page_load(time) {
    datas.top.date = new Date(JSON.parse(JSON.stringify(time)));
    datas.top.done = false;

    datas.bottom.date = new Date(JSON.parse(JSON.stringify(time)));
    datas.bottom.done = false;

    console.log(datas.bottom.date)

    load_data({
        ft: make_filter(),
        date: datas.bottom.date.format("yyyyMMdd"),
        time: datas.bottom.date.format("HHmm"),
        asc: "asc"
    }, (data) => { $("#loop").append(data) }, on_scroll_bottom,
        () => { datas.bottom.done = true; });
    on_scroll_top(true)
}

$(window).on("load", () => {
    $("#select-mall").on("change", (e) => {
        filter_mall = $("#select-mall option:selected").val()

        $("#loop").empty();

        on_page_load(datas.current_time);
    });

    $("#select-category").on("change", (e) => {
        filter_ct = $("#select-category option:selected").val()

        $("#loop").empty();

        on_page_load(datas.current_time);
    });

    load_header();
    

    $(".date-selector .date").on("click", (e) => {
        var date = $(e.target).attr("data-date");

        var year = date.substr(0, 4);
        var month = date.substr(4, 2);
        var day = date.substr(6, 2);

        var time = new Date(year, month, day);

        $("#loop").empty();

        on_page_load(time);
    });

    on_page_load(datas.current_time);
});

function on_scroll_bottom(force = false) {
    if (is_loading && !force) {
        return;
    }

    if (datas.bottom.done) {
        return;
    }

    datas.bottom.date.setHours(datas.bottom.date.getHours() + 4);

    console.log("on_scroll_bottom", datas.bottom.date);


    load_data({
        ft: make_filter(),
        date: datas.bottom.date.format("yyyyMMdd"),
        time: datas.bottom.date.format("HHmm"),
        asc: "asc"
    }, (data) => { $("#loop").append(data) }, on_scroll_bottom,
        () => { datas.bottom.done = true; });
}

function on_scroll_top(force = false) {
    if (is_loading && !force) {
        return;
    }

    if (datas.top.done) {
        return;
    }

    datas.top.date.setHours(datas.top.date.getHours() - 4);

    console.log("on_scroll_top", datas.top.date);

    load_data({
        ft: make_filter(),
        date: datas.top.date.format("yyyyMMdd"),
        time: datas.top.date.format("HHmm"),
        asc: "asc"
    }, (data) => {
        var temp = $(document).height();
        $("#loop").prepend(data)
        $(document).scrollTop($(document).height() - temp);
    }, on_scroll_top,
        () => { datas.top.done = true; });
}

$(window).scroll(() => {
    if (is_loading === false) {
        var percent = percentage($(window).scrollTop(), $(document).height() - $(window).height());
        if (percent > 80) {
            // scroll bottom

            on_scroll_bottom()
        } else if (percent < 20) {
            // scroll top

            on_scroll_top();
        }
    }
});