import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Home, BookOpen, TrendingUp, User, CircleUser, LogOut } from "lucide-react";
import { useTranslation } from "react-i18next";

  return (
    <aside className="w-full md:w-64 bg-white md:fixed md:inset-y-0 border-r border-gray-100 flex flex-col z-20">
      <div className="p-6 flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-600 rounded-xl flex items-center justify-center">
          <img src="/logo.png" className="w-5 h-5 opacity-90" alt="logo" onError={(e) => e.target.style.display='none'} />
        </div>
        <span className="font-bold text-xl text-slate-800 tracking-tight">Smart Attend</span>
      </div>

      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        <NavItem
          icon={LayoutDashboard}
          label="Home"
          active={activePage === 'dashboard'}
          path="/student-dashboard"
        />
        <NavItem
          icon={BookOpen}
          label="Subjects"
          active={activePage === 'subjects'}
          path="/student-subjects"
        />
        <NavItem
          icon={TrendingUp}
          label="Forecast"
          active={activePage === 'forecast'}
          path="/student-forecast"
        />
        <NavItem
          icon={User}
          label="Profile"
          active={activePage === 'profile'}
          path="/student-profile"
        />
      </nav>

      <div className="p-4 border-t border-gray-100">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 w-full text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 group font-medium text-sm"
        >
          <LogOut size={18} className="group-hover:scale-110 transition-transform" />
          Logout
        </button>
      </div>
    </aside>
  );
}

StudentNavigation.propTypes = {
  activePage: PropTypes.string.isRequired,
};

function NavItem({ icon: Icon, label, active, path }) {
  return (
    <Link
      to={path}
      className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium text-sm ${
        active
          ? "bg-blue-50 text-blue-600 shadow-sm shadow-blue-100"
          : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
      }`}
    >
      <Icon
        size={18}
        className={`transition-transform duration-200 ${
          active ? "scale-110" : "group-hover:scale-110"
        }`}
      />
      {label}
    </Link>
  );
}

/* ---------------------- MAIN NAVIGATION ---------------------- */
export default function StudentNavigation({ activePage = "home" }) {
  const { t } = useTranslation();
  const [username] = useState(() => {
    try {
      const stored = localStorage.getItem("user");
      return stored ? JSON.parse(stored).name : "";
    } catch {
      return "";
    }
  });

  const navigate = useNavigate();

  const navItems = [
    { id: "home", label: t('student_dashboard.nav.home'), icon: Home, path: "/student-dashboard" },
    { id: "subjects", label: t('student_dashboard.nav.subjects'), icon: BookOpen, path: "/student-subjects" },
    { id: "forecast", label: t('student_dashboard.nav.forecast'), icon: TrendingUp, path: "/student-forecast" },
    { id: "profile", label: t('student_dashboard.nav.profile'), icon: User, path: "/student-profile" },
  ];

  return (
    <>
      {/* DESKTOP SIDEBAR */}
      <aside className="hidden md:flex w-64 bg-white border-r border-gray-200 flex-col fixed h-full z-10">
        <div className="p-6 flex items-center gap-3">
          <img className="w-14 h-14 rounded-full" src="logo.png" alt="" />
          <span className="font-bold text-lg tracking-tight">{t('student_dashboard.nav.app_name')}</span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {navItems.map(item => (
            <DesktopItem
              key={item.id}
              icon={item.icon}
              label={item.label}
              path={item.path}
              active={activePage === item.id}
            />
          ))}
        </nav>

        <div className="flex items-center justify-between p-4 border-t border-gray-100 mb-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
              <CircleUser size={24} strokeWidth={2} />
            </div>
            <div>
              <p className="text-sm font-bold">{username}</p>
              <p className="text-xs text-gray-500">{t('student_dashboard.nav.student_role')}</p>
            </div>
          </div>
          <div className="logout">
            <LogOut className="cursor-pointer"  onClick={()=>{
              localStorage.setItem("user", null);
              navigate("/");
            }}/>
          </div>
        </div>

      </aside>

      {/* MOBILE BOTTOM NAVBAR */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-6 py-3 pb-6 flex justify-between items-center z-50">
        {navItems.map(item => (
          <MobileItem
            key={item.id}
            icon={item.icon}
            label={item.label}
            path={item.path}
            active={activePage === item.id}
          />
        ))}
      </div>

      <div className="md:hidden h-20"></div>
    </>
  );
}
